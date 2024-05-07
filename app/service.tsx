import * as fs from "fs";
import * as path from "path";
import { parse } from 'csv-parse';

const DATA_H_PATH = path.resolve(__dirname, 'data/scores/20240421_h.csv');
const DATA_A_PATH = path.resolve(__dirname, 'data/scores/20240421_a.csv');
const CSV_HEADERS = ['stop_id', 'score', 'address', 'latitude', 'longitude']

function readData(){
    const fileContentA = fs.readFileSync(DATA_A_PATH, { encoding: 'utf-8' })
    const fileContentH = fs.readFileSync(DATA_H_PATH, { encoding: 'utf-8' })
  
  }