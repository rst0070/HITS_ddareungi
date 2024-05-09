'use client'
import { useState } from "react";
import { StopInfo } from "@/app/types";
import Container from "@/components/Container";

const descH = ""

function TextDesc(props: {title:string, desc:string}){
    return (
        <div className="text-desc">
            <h2 className="desc-title">{props.title}</h2>
            <div className="desc-text">{props.desc}</div>
        </div>
    );
}



export default function Contents(props: {HScore:StopInfo[], AScore:StopInfo[]}){

    const [isHScore, setIsHScore] = useState(true)

  return (
    <>
        <div className="maps-wrapper">
            <TextDesc title="정보" desc="test"/>
            <Container title='몰림 정류장 정보' category='ascore' scores={props.AScore} />
            <div></div>
            <Container title='부족 정류장 정보' category='hscore' scores={props.HScore} />
        </div>
        
    </>
  );
}