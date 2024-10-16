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
        email: Yup.string().email('Email inválido').required('Email é obrigatório'),
        password: Yup.string().min(6, 'A senha deve ter pelo menos 6 caracteres').required('Senha é obrigatória'),
        confirmPassword: Yup.string().required("Senha é obrigatória"),
    });

    const sendForm = (values: { email: string; password: string; confirmPassword: string}) => {
        console.log('Dados enviados:', values);
        router.push('./'); // Redireciona após validação bem-sucedida
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