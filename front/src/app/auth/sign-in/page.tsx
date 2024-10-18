"use client";

import Button from "@/components/button";
import InputField from "@/components/inputField";
import Tittle from "@/components/tittle";
import Link from "next/link";
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import { useRouter } from "next/navigation";

export default function SignIn(){
    const router = useRouter();

    const validationSchema = Yup.object({
        email: Yup.string().email('Email inválido').required('Campo obrigatório'),
        password: Yup.string().min(6, 'A senha deve ter pelo menos 6 caracteres').required('Campo obrigatório'),
        confirmPassword: Yup.string().oneOf([Yup.ref('password'), null], 'As senhas precisam ser iguais').required('Campo obrigatório'),
    });

    const sendForm = async (values: { email: string; password: string; confirmPassword: string }) => {
        try {
            const response = await fetch("colocar url da api aqui", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username: values.email.split('@')[0], email: values.email, password: values.password }),
            });

            if (!response.ok) {
                throw new Error("Erro ao criar conta.");
            }

            const data = await response.json();
            localStorage.setItem('token', data.access_token);
            router.push('./');
        } catch (error) {
            console.error('Erro:', error);
            alert(error.message);
        }
    };
    
    return(
        <div className="flex flex-col items-center gap-[56px]">
            <div className=" w-full flex flex-col gap-[16px]">
                <div className="flex items-center gap-[28px]">
                    <Link href="./" passHref className="flex items-center">
                        <button className="bg-[url('/Vector.svg')] min-w-[12px] h-[20px]"/>
                    </Link>
                    <Tittle text='Crie a sua conta'></Tittle>
                </div>

                <Formik 
                initialValues={{ email: '', password: '', confirmPassword: '' }}
                validationSchema={validationSchema}
                onSubmit={(values) => sendForm(values)}>
                    {({ handleSubmit }) => (
                        <Form className="w-full flex flex-col items-center gap-[26px]">
                            <div className="w-full flex flex-col items-center gap-[12px]">
                                <div className="w-full">
                                    <Field name="email" placeholder="Insira seu email" tittle="Email" component={InputField} />
                                    <ErrorMessage name="email" component="div" className="text-red-500" />
                                </div>
                                <div className="w-full">
                                    <Field name="password" placeholder="Crie uma senha forte" tittle="Senha" component={InputField} />
                                    <ErrorMessage name="password" component="div" className="text-red-500" />
                                </div>
                                <div className="w-full">
                                    <Field name="confirmPassword" placeholder="Confirme sua senha" tittle="Confirmar senha" component={InputField} />
                                    <ErrorMessage name="confirmPassword" component="div" className="text-red-500" />
                                </div>
                            </div>
                            
                            <div className="w-[80%]">
                                <Button text="Continuar" variant="primary" type="submit" />
                            </div>
                        </Form>
                    )}
                </Formik>
            </div>
        </div>
    )
}