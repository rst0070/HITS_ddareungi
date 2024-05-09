import {HScore, AScore} from './service'
import Container from "@/components/Container";


export default function Home() {
  let date = '2024.05.09'
  return (
    <>
      <p className="navBar">따릉이 부족, 넘침 점수 {date}기준</p>
      <center>
        <Container title="부족점수" scores={HScore} />
        <Container title="넘침점수" scores={AScore} />
      </center>      
    </>
  );
}
