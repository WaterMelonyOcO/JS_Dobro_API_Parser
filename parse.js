import { parse } from "json2csv";
import * as fs from "fs";

async function del(region = 0, year = 0) {
  return fetch(`https://dobro.ru/api/v2/analytics/get?region=${region}&year=${year}`)
    .then((res) => res)
    .then(data => {
      // console.log(data);
      // fs.writeFile("./data.json", JSON.stringify(data), (err) => {
      //   if (err) { console.log(err) }
      // })
      return data.json();
    })
}

async function writerAllData(UpData = true) {
  let yesrs = [0, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
  // let yesrs = [0]
  let region = Array.from({ length: 2 }, (_, index) => index++)

  let jsonData = {}

  if (UpData) {

    for await (let i of region) {
      jsonData[i] = {};
      for await (let j of yesrs) {
        jsonData[i][j] = await del(0, j)
      }
    }

    fs.writeFile("./data.json", JSON.stringify(jsonData), (err) => {
      if (err) { console.log(err) }
    })
  }

  else{
    jsonData = fs.readFileSync("data.json", "utf-8", (err)=>{console.log(err);})
    jsonData = JSON.parse(jsonData)
  }
  let csv = parse(jsonData, {delimiter: "-"})

  fs.writeFile("./data.csv", csv, (err) => {
    if (err) { console.log(err) }
  })
}

writerAllData(false)


