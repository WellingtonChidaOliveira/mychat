import Image from "next/image";

type DownloadButtonProps = {
    className: string;
}
export default function DownloadButton({className}: DownloadButtonProps){
    return(
        <button className={className}>
            <Image src="/download.svg" alt='download' width={30} height={30}></Image>
        </button>
    )
}
