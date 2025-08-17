import React, { useState } from 'react';
import { ParentRegistrationForm } from '../components/auth/ParentRegistrationForm';
import { RegistrationSuccess } from '../components/auth/RegistrationSuccess';

export const RegisterPage: React.FC = () => {
  const [registeredEmail, setRegisteredEmail] = useState<string | null>(null);

  const handleRegistrationSuccess = (email: string) => {
    setRegisteredEmail(email);
  };

  const handleBackToRegistration = () => {
    setRegisteredEmail(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md mx-auto">
        {!registeredEmail ? (
          <>
            <ParentRegistrationForm onSuccess={handleRegistrationSuccess} />
            
            {/* Additional Info Section */}
            <div className="mt-8 bg-white p-6 rounded-lg shadow-sm">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">
                Why Join ClassDojo?
              </h2>
              <ul className="space-y-3 text-sm text-gray-600">
                <li className="flex items-start">
                  <svg className="w-5 h-5 text-primary-500 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  <span>Real-time updates on your child's activities and progress</span>
                </li>
                <li className="flex items-start">
                  <svg className="w-5 h-5 text-primary-500 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  <span>Direct messaging with teachers and staff</span>
                </li>
                <li className="flex items-start">
                  <svg className="w-5 h-5 text-primary-500 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  <span>Photo and video sharing of memorable moments</span>
                </li>
                <li className="flex items-start">
                  <svg className="w-5 h-5 text-primary-500 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  <span>Easy scheduling and calendar management</span>
                </li>
              </ul>
            </div>
          </>
        ) : (
          <RegistrationSuccess email={registeredEmail} />
        )}
      </div>
    </div>
  );
};