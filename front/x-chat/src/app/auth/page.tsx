"use client";

import Link from 'next/link';
import InputField from '@/components/inputField';
import Button from '@/components/button';

export default function auth(){

    const sendForm = () => {
        return //adicionar logica para conectar ao back
    }


    return(
        <div className='w-full h-full flex flex-col items-center gap-[32px] mb-[10%]'>
            <h1 className="text-2xl font-medium leading-[36px] font-poppins text-[#333333]">Faça seu login ou crie uma conta</h1>

            <div className="w-full flex flex-col gap-[12px]">
                <InputField placeholder="E-mail"/>
                <InputField placeholder="Senha"/>

                <div className="flex justify-between w-full">
                    <div className="flex gap-2">
                        <input type="checkbox" className="accent-[#589b97a1]" />
                        <p className="text-[#372F30]">Lembrar-me</p>
                    </div>
                    <Link href='/auth/password' passHref>
                        <button className="text-[#372F30] underline">Esqueceu sua senha?</button>
                    </Link>
                    
                </div>
            </div>

            <div className="w-[80%] flex flex-col gap-[16px]">
                <Button href="./" text="Entrar" variant="primary" onClick={sendForm}/>
                <Button href="/auth/sign-in" text="Cadastre-se" variant="secundary"/>
            </div>
        </div>
    )
}