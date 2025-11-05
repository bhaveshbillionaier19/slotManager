import React, { createContext, useCallback, useEffect, useMemo, useState } from 'react';
import { jwtDecode } from 'jwt-decode';
import { getToken, setToken as storeToken, removeToken } from '@/utils/auth';
import { TokenPayload, User } from '@/types';

type AuthContextType = {
  user: User | null;
  token: string | null;
  loading: boolean;
  login: (accessToken: string) => void;
  logout: () => void;
  checkAuth: () => void;
};

export const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [token, setToken] = useState<string | null>(null);
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true); // Start in a loading state

  const applyToken = useCallback((t: string | null) => {
    setToken(t);
    if (t) {
      try {
        const decoded = jwtDecode<TokenPayload>(t);
        const u: User = { id: decoded.user_id, email: '', name: '' };
        setUser(u);
      } catch {
        setUser(null);
      }
    } else {
      setUser(null);
    }
  }, []);

  const checkAuth = useCallback(() => {
    try {
      const stored = getToken();
      applyToken(stored);
    } finally {
      setLoading(false); // End loading state after check
    }
  }, [applyToken]);

  const login = useCallback((accessToken: string) => {
    storeToken(accessToken);
    applyToken(accessToken);
  }, [applyToken]);

  const logout = useCallback(() => {
    removeToken();
    applyToken(null);
  }, [applyToken]);

  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  const value = useMemo<AuthContextType>(
    () => ({ user, token, loading, login, logout, checkAuth }),
    [user, token, loading, login, logout, checkAuth]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};


