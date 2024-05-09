'use client'
import { MouseEventHandler, useState } from "react";
import { StopInfo, CenterInfo } from "@/app/types";
import KakaoMap from "./KakaoMap";

function StopElement(props: {stopInfo:StopInfo, clickListener:Function}){
    const handleClick: MouseEventHandler = (event) => {
        props.clickListener(props.stopInfo)
    };

    return (
      <li className="stop_element" onClick={handleClick}>
        <div className="stop_element_order">{props.stopInfo.rank}</div>
        <div className="stop_element_score">{props.stopInfo.score}</div>
        <div className="stop_element_addr">{props.stopInfo.address}</div>
      </li>
    )
}
  
function StopList(props: {stopList:StopInfo[], category:string, clickListener:Function}){
    let el_list = []
    for(let i=0; i < props.stopList.length; i++)
      el_list.push(<StopElement key={props.stopList[i].stop_id+props.category} stopInfo={props.stopList[i]} clickListener={props.clickListener}/>)
  
    return (
      <ul className="stop_scroll">
        <li className="stop_element">
          <div className="stop_element_order">순위</div>
          <div className="stop_element_score">점수</div>
          <div className="stop_element_addr">주소</div>
        </li>
        {el_list}
      </ul>
    )
}


export default function Container(props: {title:string, scores:StopInfo[], category:string}){

    let initialCenterInfo: CenterInfo = {id: props.scores[0].stop_id, latitude: props.scores[0].latitude, longitude: props.scores[0].longitude}
    
    const [centerInfo, setCenterInfo] = useState(initialCenterInfo)

    const handleClick:Function = (stopInfo:StopInfo) =>{
      setCenterInfo({
        id: stopInfo.stop_id,
        latitude: stopInfo.latitude,
        longitude: stopInfo.longitude
      })
    }

    return (
        <div className="contents-container">
            <KakaoMap stopList={props.scores} centerInfo={centerInfo}/>
            <StopList stopList={props.scores} category={props.category} clickListener={handleClick}/>
        </div>
    );
}