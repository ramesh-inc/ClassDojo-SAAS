# core/migrations/0011_add_custom_indexes.py
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0010_populate_learning_activities'),
    ]

    operations = [
        # MySQL-compatible way to create indexes safely
        migrations.RunSQL(
            """
            SET @sql = (SELECT IF(
                (SELECT COUNT(*) FROM INFORMATION_SCHEMA.STATISTICS 
                 WHERE table_schema = DATABASE() 
                 AND table_name = 'daily_attendance' 
                 AND index_name = 'idx_attendance_date_class') = 0,
                'CREATE INDEX idx_attendance_date_class ON daily_attendance (attendance_date, class_obj_id)',
                'SELECT "Index already exists"'
            ));
            PREPARE stmt FROM @sql;
            EXECUTE stmt;
            DEALLOCATE PREPARE stmt;
            """,
            reverse_sql="DROP INDEX idx_attendance_date_class ON daily_attendance;"
        ),

        migrations.RunSQL(
            """
            SET @sql = (SELECT IF(
                (SELECT COUNT(*) FROM INFORMATION_SCHEMA.STATISTICS 
                 WHERE table_schema = DATABASE() 
                 AND table_name = 'posts' 
                 AND index_name = 'idx_posts_created_featured') = 0,
                'CREATE INDEX idx_posts_created_featured ON posts (created_at, is_featured, is_deleted)',
                'SELECT "Index already exists"'
            ));
            PREPARE stmt FROM @sql;
            EXECUTE stmt;
            DEALLOCATE PREPARE stmt;
            """,
            reverse_sql="DROP INDEX idx_posts_created_featured ON posts;"
        ),

        # Fulltext index with safe creation
        migrations.RunSQL(
            """
            SET @sql = (SELECT IF(
                (SELECT COUNT(*) FROM INFORMATION_SCHEMA.STATISTICS 
                 WHERE table_schema = DATABASE() 
                 AND table_name = 'students' 
                 AND index_name = 'student_name') = 0,
                'ALTER TABLE students ADD FULLTEXT(student_name)',
                'SELECT "Fulltext index already exists"'
            ));
            PREPARE stmt FROM @sql;
            EXECUTE stmt;
            DEALLOCATE PREPARE stmt;
            """,
            reverse_sql="ALTER TABLE students DROP INDEX student_name;"
        ),
    ]