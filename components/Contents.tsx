import { StopInfo } from "@/app/types";
import Container from "@/components/Container";


function TextDesc(props: {title:string, desc:string}){
    let descList = props.desc.split('  \n')

    return (
        <div className="text-desc">
            <h2 className="desc-title">{props.title}</h2>
            <div className="desc-text">
                {
                    descList.map((str, idx) => 
                        <p key={"desc-element:"+props.title+":idx:"+idx}>{str}</p>
                    )
                }
            </div>
        </div>
    );
}

const desc_algorithm = 
`
HITS(Hub and Authorities algorithm) 알고리즘은 웹페이지간의 링크정보를 이용하여, 어떤 웹페이지의 중요도를 표현하는 알고리즘입니다. 
이 알고리즘은 중요한 페이지를 두가지로 분류합니다.  
- Hub: 허브는 좋은 컨텐츠를 가진 여러 웹 페이지(즉, Authority 페이지)로 이어주는 역할을 하는 웹 페이지.  
- Authority (권위자): 권위자는 특정 주제에 대해 우수한 컨텐츠를 제공하는 웹 페이지로, 여러 좋은 허브 페이지들로부터 링크를 많이 받습니다.  
  
위 개념을 따릉이 대여소에 적용하면 각 따릉이 대여소를 Hub와 Authority로 구분해 볼 수 있습니다.  
- Hub: 여러 Authority 대여소로 많이 따릉이를 보내는 대여소, 즉 따릉이가 몰리는곳으로 따릉이를 많이 보내는 대여소  
- Authority: 여러 허브 대여소로 부터 따릉이를 많이 받는 대여소, 즉 따릉이가 많이 나오는곳에서 부터 따릉이를 많이 받는 대여소  
  
리스트의 각 요소를 클릭하면 지도가 해당 대여소의 위치로 이동합니다.  
지도위에서 대여소는 점수가 높은 대여소 부터 낮은 대여소까지 빨간색, 주황색, 노란색 녹색 마커로 표현됩니다.
`

const desc_authority_score = 
`
리스트는 Authority 점수가 높은 대여소부터 낮은 대여소로 각 대여소의 주소와 점수를 보여줍니다.  
Authority점수가 높을수록, 따릉이가 많이 대여되는곳으로 부터 온 따릉이가 
해당 대여소에서 반납됨을 나타냅니다. 
`

const desc_hub_score = 
`
리스트는 Hub 점수가 높은 대여소부터 낮은 대여소로 각 대여소의 주소와 점수를 보여줍니다.  
Hub점수가 높은것은, 해당 대여소에서 따릉이가 대여되어, 따릉이가 많이 반납되는되는곳으로 반납됨을 나타냅니다. 
`

export default function Contents(props: {HScore:StopInfo[], AScore:StopInfo[]}){

  return (
    <>
        <div className="maps-wrapper">
            <TextDesc title="HITS 알고리즘" desc={desc_algorithm}/>
            <div style={{height: '50px'}}></div>

            <TextDesc title="Authority Score" desc={desc_authority_score}/>
            <Container title='Authority score별 대여소' category='ascore' scores={props.AScore} />
            <div></div>

            <TextDesc title="Hub Score" desc={desc_hub_score}/>
            <Container title='Hub score별 대여소' category='hscore' scores={props.HScore} />
        </div>
        
    </>
  );
}