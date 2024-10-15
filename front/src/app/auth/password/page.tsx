import Button from "@/components/button";
import InputField from "@/components/inputField";

export default function SignIn(){
    const sendForm = () => {
        return //adicionar logica para conectar ao back
    }

    return(
        <div className="flex flex-col items-center gap-[42px]">
            <div className="flex flex-col items-center">
                <span className="text-[30px] font-semibold leading-[37.5px] font-poppins text-[#3ea59f]">Esqueceu a sua senha?</span>
                <span className="text-[30px] font-semibold leading-[37.5px] font-poppins text-[#3ea59f]">Sem problemas!</span>
            </div>

            <div className=" w-full flex flex-col gap-[16px]">
                <p className="text-[18px] font-normal leading-[27px] font-poppins text-[#333333]">
                    Insira o seu endereço de e-mail para receber um código para redefinir sua senha.
                </p>
                <InputField placeholder="Email" tittle="Seu endereço de e-mail"/>
            </div>

            <div className="flex flex-col w-[80%] gap-[16px]">
                <Button href="/auth/password/code" text="Enviar Código" variant="primary" onClick={sendForm}/>
                <Button href="./" text="Voltar" variant="secundary"/>
            </div>
        </div>
        

        
    )
}