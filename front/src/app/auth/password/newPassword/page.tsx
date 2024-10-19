"use client";

import Button from "@/components/button";
import InputField from "@/components/inputField";
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import { useRouter } from "next/navigation";

export default function SignIn(){
    const router = useRouter();

    const validationSchema = Yup.object({
        password: Yup.string().min(6, 'A senha deve ter pelo menos 6 caracteres').required('Campo obrigatório'),
        confirmPassword: Yup.string().oneOf([Yup.ref('password'), undefined], 'As senhas precisam ser iguais').required('Campo obrigatório'),
    });

    const sendForm = (values: { password: string; confirmPassword: string }) => {
        console.log('Dados enviados:', values);
        router.push('/auth');
    };
    return(
        <div className="flex flex-col items-center gap-[42px]">
            <span className="text-[30px] font-semibold leading-[37.5px] font-poppins text-[#3ea59f]">Nova senha</span>
            <Formik 
                initialValues={{ password: '', confirmPassword: '' }}
                validationSchema={validationSchema}
                onSubmit={(values) => sendForm(values)}>
                {({ handleSubmit }) => (
                    <Form className=" w-full flex flex-col items-center gap-[42px]" onSubmit={handleSubmit}>
                        <div className=" w-full flex flex-col gap-[16px]">
                            <p className="text-[18px] font-normal leading-[27px] font-poppins text-[#333333]">
                                Insira uma nova senha para a sua conta.
                            </p> 
                            <div>
                                <Field name="password" placeholder="Crie uma senha forte" tittle="Nova senha" component={InputField} />
                                <ErrorMessage name="password" component="div" className="text-red-500" />
                            </div>
                            <div>
                                <Field name="confirmPassword" placeholder="Confirmar senha" tittle="Confirmar senha" component={InputField} />
                                <ErrorMessage name="confirmPassword" component="div" className="text-red-500" />
                            </div>
                        </div>
                        <div className="w-[80%]">
                            <Button text="Continuar" variant="primary" type="submit"/>
                        </div>
                    </Form>
                )}
            </Formik>
        </div>
    )
}