import { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { Container, CircularProgress, Typography, Alert, Box } from '@mui/material';
import { microsoftAPI } from '../services/api';

const Callback = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [status, setStatus] = useState('processing'); // processing, success, error
  const [message, setMessage] = useState('Procesando autenticación...');

  useEffect(() => {
    const handleCallback = async () => {
      try {
        const token = searchParams.get('token');
        const error = searchParams.get('error');

        if (error) {
          setStatus('error');
          setMessage(`Error de autenticación: ${error}`);
          return;
        }

        if (!token) {
          setStatus('error');
          setMessage('No se recibió el token de autenticación');
          return;
        }

        // Guardar el token JWT directamente
        localStorage.setItem('token', token);
        
        // Obtener información del usuario desde el token
        try {
          const payload = JSON.parse(atob(token.split('.')[1]));
          const user = {
            id: payload.sub,
            name: 'Usuario Microsoft',
            email: 'usuario@microsoft.com'
          };
          localStorage.setItem('user', JSON.stringify(user));
        } catch (e) {
          console.warn('No se pudo decodificar el token, usando datos por defecto');
          const user = {
            id: 'microsoft-user',
            name: 'Usuario Microsoft',
            email: 'usuario@microsoft.com'
          };
          localStorage.setItem('user', JSON.stringify(user));
        }
        
        setStatus('success');
        setMessage('¡Autenticación exitosa! Redirigiendo...');
        
        // Redirigir al dashboard después de 2 segundos
        setTimeout(() => {
          navigate('/dashboard');
        }, 2000);
        
      } catch (error) {
        console.error('Error en callback:', error);
        setStatus('error');
        setMessage('Error al procesar la autenticación');
      }
    };

    handleCallback();
  }, [searchParams, navigate]);

  return (
    <Container component="main" maxWidth="sm">
      <Box
        sx={{
          marginTop: 8,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          textAlign: 'center'
        }}
      >
        {status === 'processing' && (
          <>
            <CircularProgress size={60} sx={{ mb: 3 }} />
            <Typography variant="h5" gutterBottom>
              {message}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Conectando con tu cuenta de Microsoft...
            </Typography>
          </>
        )}

        {status === 'success' && (
          <>
            <Alert severity="success" sx={{ mb: 3, width: '100%' }}>
              {message}
            </Alert>
            <Typography variant="body2" color="text.secondary">
              Te estamos redirigiendo al dashboard...
            </Typography>
          </>
        )}

        {status === 'error' && (
          <>
            <Alert severity="error" sx={{ mb: 3, width: '100%' }}>
              {message}
            </Alert>
            <Typography 
              variant="body2" 
              color="primary" 
              onClick={() => navigate('/')}
              sx={{ cursor: 'pointer', textDecoration: 'underline' }}
            >
              Volver a intentar
            </Typography>
          </>
        )}
      </Box>
    </Container>
  );
};

export default Callback;