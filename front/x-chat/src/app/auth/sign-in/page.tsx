"use client";

import Button from "@/components/button";
import InputField from "@/components/inputField";
import Tittle from "@/components/tittle";
import Link from "next/link";

export default function SignIn(){
    const sendForm = () => {
        return //adicionar logica para conectar ao back
    }

    return(
        <div className="flex flex-col items-center gap-[56px]">
            <div className=" w-full flex flex-col gap-[16px]">
                <div className="flex items-center gap-[28px]">
                    <Link href="./" passHref className="flex items-center">
                        <button className="bg-[url('/Vector.svg')] min-w-[12px] h-[20px]"/>
                    </Link>
                    <Tittle text='Crie a sua conta'></Tittle>
                </div>
                
                <InputField placeholder="Insira seu email" tittle="Email"/>
                <InputField placeholder="Crie uma senha forte" tittle="Senha"/>
                <InputField placeholder="Confirme sua senha" tittle="Confirmar senha"/>
            </div>
            <div className="w-[80%]">
                <Button href="./" text="Continuar" variant="primary" onClick={sendForm}/>
            </div>
        </div>
    )
}