type TextProps = {
    text: string;
}

export default function Tittle({text} : TextProps){
    return(
        <h1 className="text-2xl font-medium leading-[36px] font-poppins text-[#333333]">{text}</h1>
    )
}