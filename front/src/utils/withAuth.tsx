import { useEffect } from 'react';
import { useRouter } from 'next/router';

type Props = {
  children: React.ReactNode;
};

const withAuth = (WrappedComponent: React.FC) => {
  const Wrapper = (props: Props) => {
    const router = useRouter();

    useEffect(() => {
      const token = localStorage.getItem('token'); // Verifique o token de autenticação (pode ser de localStorage, cookie, etc.)

      if (!token) {
        // Se o usuário não estiver autenticado, redirecione para a página de login
        router.replace('/login');
      }
    }, [router]);

    // Enquanto a verificação de autenticação ocorre, você pode renderizar um loader ou nada
    return <p>Carregando...</p>;
  };

  return Wrapper;
};

export default withAuth;
