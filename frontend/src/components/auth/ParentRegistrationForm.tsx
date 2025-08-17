import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import { parentRegistrationSchema, ParentRegistrationFormData } from '../../utils/validation';
import { authApi } from '../../services/api';
import { FormField } from '../ui/FormField';
import { LoadingSpinner } from '../ui/LoadingSpinner';
import { ApiError } from '../../types/auth';

interface ParentRegistrationFormProps {
  onSuccess?: (email: string) => void;
}

export const ParentRegistrationForm: React.FC<ParentRegistrationFormProps> = ({
  onSuccess,
}) => {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors, isValid },
    setError,
    clearErrors,
  } = useForm<ParentRegistrationFormData>({
    resolver: yupResolver(parentRegistrationSchema),
    mode: 'onBlur',
    defaultValues: {
      firstName: '',
      lastName: '',
      email: '',
      mobileNo: '',
      preferredLanguage: 'en',
      password: '',
      confirmPassword: '',
    },
  });

  const onSubmit = async (data: ParentRegistrationFormData) => {
    setIsSubmitting(true);
    setSubmitError(null);
    clearErrors();

    try {
      const response = await authApi.registerParent(data);
      
      // Registration successful
      if (onSuccess) {
        onSuccess(data.email);
      }
    } catch (error: any) {
      console.error('Registration failed:', error);

      if (error.response?.data) {
        const errorData: ApiError = error.response.data;
        
        // Handle field-specific errors
        if (errorData.errors) {
          Object.entries(errorData.errors).forEach(([field, messages]) => {
            const fieldName = field === 'first_name' ? 'firstName' :
                            field === 'last_name' ? 'lastName' :
                            field === 'mobile_no' ? 'mobileNo' :
                            field === 'preferred_language' ? 'preferredLanguage' :
                            field === 'confirm_password' ? 'confirmPassword' :
                            field;
            
            if (fieldName in data) {
              setError(fieldName as keyof ParentRegistrationFormData, {
                type: 'server',
                message: messages[0],
              });
            }
          });
        }
        
        // Handle general error message
        if (errorData.message) {
          setSubmitError(errorData.message);
        }
      } else if (error.message) {
        setSubmitError(error.message);
      } else {
        setSubmitError('Registration failed. Please try again.');
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  const languageOptions = [
    { value: 'en', label: 'English' },
    { value: 'si', label: 'සිංහල (Sinhala)' },
    { value: 'ta', label: 'தமிழ் (Tamil)' },
  ];

  return (
    <div className="max-w-md mx-auto bg-white p-8 rounded-lg shadow-lg">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Create Parent Account
        </h1>
        <p className="text-gray-600">
          Join ClassDojo to stay connected with your child's learning journey
        </p>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6" noValidate>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <FormField
            label="First Name"
            name="firstName"
            placeholder="Enter your first name"
            required
            error={errors.firstName?.message}
            {...register('firstName')}
          />

          <FormField
            label="Last Name"
            name="lastName"
            placeholder="Enter your last name"
            required
            error={errors.lastName?.message}
            {...register('lastName')}
          />
        </div>

        <FormField
          label="Email Address"
          name="email"
          type="email"
          placeholder="Enter your email address"
          required
          error={errors.email?.message}
          {...register('email')}
        />

        <FormField
          label="Mobile Number"
          name="mobileNo"
          type="tel"
          placeholder="Enter your mobile number (e.g., +94771234567)"
          required
          error={errors.mobileNo?.message}
          {...register('mobileNo')}
        />

        <FormField
          label="Preferred Language"
          name="preferredLanguage"
          required
          error={errors.preferredLanguage?.message}
          {...register('preferredLanguage')}
        >
          <select className="form-input">
            {languageOptions.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </FormField>

        <FormField
          label="Password"
          name="password"
          type="password"
          placeholder="Create a strong password"
          required
          error={errors.password?.message}
          {...register('password')}
          aria-describedby="password-requirements"
        />

        <div id="password-requirements" className="text-sm text-gray-600 bg-gray-50 p-3 rounded">
          <p className="font-medium mb-1">Password requirements:</p>
          <ul className="list-disc list-inside space-y-1">
            <li>At least 8 characters long</li>
            <li>One uppercase letter (A-Z)</li>
            <li>One lowercase letter (a-z)</li>
            <li>One number (0-9)</li>
            <li>One special character (@$!%*?&)</li>
          </ul>
        </div>

        <FormField
          label="Confirm Password"
          name="confirmPassword"
          type="password"
          placeholder="Confirm your password"
          required
          error={errors.confirmPassword?.message}
          {...register('confirmPassword')}
        />

        {submitError && (
          <div className="bg-error-50 border border-error-200 text-error-700 px-4 py-3 rounded" role="alert">
            {submitError}
          </div>
        )}

        <button
          type="submit"
          disabled={isSubmitting || !isValid}
          className="btn-primary w-full flex items-center justify-center"
          aria-describedby={isSubmitting ? "submitting-status" : undefined}
        >
          {isSubmitting ? (
            <>
              <LoadingSpinner size="sm" className="mr-2" />
              <span id="submitting-status">Creating Account...</span>
            </>
          ) : (
            'Create Account'
          )}
        </button>

        <div className="text-center">
          <p className="text-sm text-gray-600">
            Already have an account?{' '}
            <a href="/login" className="text-primary-600 hover:text-primary-700 font-medium">
              Sign in here
            </a>
          </p>
        </div>
      </form>

      <div className="mt-6 text-xs text-gray-500 text-center">
        <p>
          By creating an account, you agree to our{' '}
          <a href="/terms" className="text-primary-600 hover:text-primary-700">
            Terms of Service
          </a>{' '}
          and{' '}
          <a href="/privacy" className="text-primary-600 hover:text-primary-700">
            Privacy Policy
          </a>
        </p>
      </div>
    </div>
  );
};