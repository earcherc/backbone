type Toast = {
  id: string;
  type: string;
  content: string; // Or JSX.Element
  autoCloseDelay: number;
  remainingTime: number;
  isPaused: boolean;
};

interface ToastType {
  bgColor: string;
  textColor: string;
  progressColor: string;
  icon: ReactElement | null;
}

interface IToastContext {
  toasts: Toast[];
  addToast: (toast: Pick<Toast, 'type' | 'content'> & Partial<Pick<Toast, 'autoCloseDelay'>>) => void;
  removeToast: (id: string) => void;
  pauseToast: (id: string) => void;
  resumeToast: (id: string) => void;
}

interface IAuthContext {
  isAuthenticated: boolean;
  username: string | null;
  userId: number | null;
  isDisabled: boolean | null;
}
