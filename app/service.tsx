import * as fs from "fs";
import * as path from "path";

const DATA_H_PATH = 'data/scores/20240421_h.csv'//path.resolve(__dirname, 'data/scores/20240421_h.csv');
const DATA_A_PATH = 'data/scores/20240421_a.csv'//path.resolve(__dirname, 'data/scores/20240421_a.csv');
const CSV_HEADERS = ['stop_id', 'score', 'address', 'latitude', 'longitude']

export type StopInfo = {
  stop_id: string,
  score: number,
  address: string,
  latitude: string,
  longitude: string
}

function createStopInfoObj(stop_id:string, score:number, address:string, latitude:string, longitude:string){
  let obj:StopInfo = {
    stop_id,
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

  for(let i = 0; i < line_data.length-1; i++){
    let data_seq = line_data[i].split(',')
    let stop_info = createStopInfoObj(data_seq[0], Number(data_seq[1]), data_seq[2], data_seq[3], data_seq[4])
    result.push(stop_info)
  }
  return result
}

const HScore = readAndSplitData(DATA_H_PATH)
const AScore = readAndSplitData(DATA_A_PATH)

export {HScore, AScore}
