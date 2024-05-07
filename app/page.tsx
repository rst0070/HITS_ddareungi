
import Image from "next/image"
import KakaoMap from "@/components/KakaoMap"
import NavBar from "@/components/NavBar";
import ModeButtons from "@/components/ModeButtons";




export default function Home() {
  return (
    <div>
      <NavBar/>
      <KakaoMap />
      <ModeButtons />

    </div>
  );
}
