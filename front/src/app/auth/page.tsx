"use client";

import Link from 'next/link';
import InputField from '@/components/inputField';
import Button from '@/components/button';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import { useRouter } from "next/navigation";

export default function auth() {
  const router = useRouter();

  const validationSchema = Yup.object({
    email: Yup.string().email('Email inválido').required('Campo obrigatório'),
    password: Yup.string().min(6, 'A senha deve ter pelo menos 6 caracteres').required('Campo obrigatório'),
  });

  const sendForm = async (values: { email: string; password: string }) => {
    try {
      const response = await fetch("http://localhost:8000/auth/login", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(values),
      });

      if (!response.ok) {
        throw new Error("Login falhou. Verifique suas credenciais.");
      }

      const data = await response.json();
      localStorage.setItem('token', data.access_token);
      router.push('./');
    } catch (error) {
      if (error instanceof Error) {
          console.error('Erro:', error.message);
          alert(error.message);
      } else {
          console.error('Erro desconhecido:', error);
          alert('Ocorreu um erro desconhecido.');
      }
  }
  };

  return (
    <div className='w-full h-full flex flex-col items-center gap-[32px] mb-[10%]'>
      <h1 className="text-2xl font-medium leading-[36px] font-poppins text-[#333333]">Faça seu login ou crie uma conta</h1>

      <Formik
        initialValues={{ email: '', password: '' }}
        validationSchema={validationSchema}
        onSubmit={(values) => sendForm(values)}>
        {({ handleSubmit }) => (
          <Form className="w-full flex flex-col items-center gap-[40px]" onSubmit={handleSubmit}>
            <div className="w-full flex flex-col gap-[12px]">
                <div>
                    <Field name="email" placeholder="E-mail" component={InputField} />
                    <ErrorMessage name="email" component="div" className="text-red-500" />
                </div>

                <div>
                    <Field name="password" type="password" placeholder="Senha" component={InputField} />
                    <ErrorMessage name="password" component="div" className="text-red-500" />
                </div>
              <div className="flex justify-between w-full">
                <div className="flex gap-2">
                  <input type="checkbox" className="accent-[#589b97a1]" />
                  <p className="text-[#372F30]">Lembrar-me</p>
                </div>
                <Link href='/auth/password' passHref className='text-[#372F30] underline'>
                    Esqueceu sua senha?
                </Link>
              </div>
            </div>

            <div className="w-[80%] flex flex-col  gap-[16px]">
              <Button text="Entrar" variant="primary" type="submit" />
              <Button href="/auth/register" text="Cadastre-se" variant="secundary" />
            </div>
          </Form>
        )}
      </Formik>
    </div>
  );
}
