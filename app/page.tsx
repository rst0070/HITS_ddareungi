
import Image from "next/image"
import KakaoMap from "@/components/KakaoMap"
import NavBar from "@/components/NavBar";
import ModeButtons from "@/components/ModeButtons";
import {HScore, AScore, StopInfo} from './service'

//console.log(HScore)

function createStopElement(stop_info:StopInfo){
  return (
    <div>
      {stop_info.score}, {stop_info.address}
    </div>
  )
}

function createStopList(stop_list:StopInfo[]){
  return (
    <div className="scroll">
      {
        stop_list.map(createStopElement)
      }
    </div>
    
  )
}

const hubElements:JSX.IntrinsicElements['div'][] = []
for(let i = 0; i < HScore.length; i++)
  hubElements.push( createStopElement(HScore[i]) )

export default function Home() {
  let HList = createStopList(HScore)
  let AList = createStopList(AScore)

  return (
    <>
      <NavBar/>
      <center>
        <div className="grid-container">
          <section className="grid-item">
            <KakaoMap />
          </section>
          <aside className="grid-item">
            {HList}
          </aside>
        </div>
        <div className="grid-container">
          <section className="grid-item">
            <KakaoMap />
          </section>
          <aside className="grid-item">
            {AList}
          </aside>
        </div>
      </center>      
    </>
  );
}
