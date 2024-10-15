type OldChatProps = {
    tittle: string;
    onClick?: () => void;
}

export default function OldChat({tittle, onClick}: OldChatProps){
    return(
        <button onClick={onClick} className="flex w-full hover:bg-zinc-600 rounded-md px-2 py-1 cursor-pointer">
            <p className="justify-self-start">{tittle}</p>
        </button>
    )
}