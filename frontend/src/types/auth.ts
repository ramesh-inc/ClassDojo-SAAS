export interface ParentRegistrationData {
  firstName: string;
  lastName: string;
  email: string;
  mobileNo: string;
  preferredLanguage: 'en' | 'si' | 'ta';
  password: string;
  confirmPassword: string;
}

export interface ApiError {
  message: string;
  errors?: {
    [key: string]: string[];
  };
}

export interface RegistrationResponse {
  message: string;
  user_id: number;
  email: string;
}