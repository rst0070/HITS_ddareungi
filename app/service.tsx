import * as fs from "fs";
import { StopInfo } from "./types";

const DATA_H_PATH = 'data/scores/20240503_h.csv'//path.resolve(__dirname, 'data/scores/20240421_h.csv');
const DATA_A_PATH = 'data/scores/20240503_a.csv'//path.resolve(__dirname, 'data/scores/20240421_a.csv');

function createStopInfoObj(stop_id:string, rank:number, score:string, address:string, latitude:number, longitude:number){
  let obj:StopInfo = {
    stop_id,
    rank,
    score,
    address,
    latitude,
    longitude
  }
  return obj
}

function readAndSplitData(data_path:string){
  let str_data = fs.readFileSync(data_path, 'utf8');
  let line_data = str_data.split('\n')
  let result = []

  for(let i = 1; i < line_data.length; i++){
    let data_seq = line_data[i].split(',')
    let stop_info = createStopInfoObj(data_seq[0], i, Number(data_seq[1]).toFixed(2), data_seq[2], Number(data_seq[3]), Number(data_seq[4]))
    result.push(stop_info)
  }
  return result
}

const HScore = readAndSplitData(DATA_H_PATH)
const AScore = readAndSplitData(DATA_A_PATH)

export {HScore, AScore}
