import Script from 'next/script'
import {HScore, AScore} from './service'
import Contents
 from '@/components/Contents';


const APP_KEY = '633117026be1caa09108a7721bed0b2d'
const KAKAO_SDK_URL = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${APP_KEY}&autoload=false`;

export default function Home() {
  let date = '2024.05.09'

  return (
    <>
      <Script src={KAKAO_SDK_URL} strategy="beforeInteractive" />
      <div className="navBar">
        <h1>따릉이HITS {date}기준</h1>
      </div>
      <Contents HScore={HScore} AScore={AScore} />
    </>
  );
}
