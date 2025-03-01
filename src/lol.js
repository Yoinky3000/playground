// const url = 'https://www48.polyu.edu.hk/myhkcc_new/me/addDrop/addDropVacy';
const data = {
  // key1: 'value1',
  // key2: 'value2'
}; // Your data object

let addDropVacy = "https://www48.polyu.edu.hk/myhkcc_new/me/addDrop/addDropVacy"

let verifyAddDrop = "https://www48.polyu.edu.hk/myhkcc_new/me/addDrop/verifyAddDrop"
let aaa = {"rgstSubj":[{"subjCode":"LCH1047","subjTtl":"ENGLISH FOR ACADEMIC STUDIES (SCIENCE AND TECHNOLOGY) II","subjType":"G","cpulOrEle":"C","cr":3,"geDmn":null,"isChnRlt":false,"teachingMode":"Blended","subjGrp":"B05","noDrop":true},{"subjCode":"SEHH1049","subjTtl":"PHYSICS I","subjType":"G","cpulOrEle":"C","cr":3,"geDmn":"Cluster D","isChnRlt":false,"teachingMode":"F2F","subjGrp":"B02B","noDrop":true},{"subjCode":"SEHH1070","subjTtl":"STATISTICS AND VECTOR ALGEBRA","subjType":"G","cpulOrEle":"C","cr":3,"geDmn":"Cluster D","isChnRlt":false,"teachingMode":"F2F","subjGrp":"B05B","noDrop":true},{"subjCode":"SEHH2041","subjTtl":"APPLIED COMPUTING","subjType":"G","cpulOrEle":"C","cr":3,"geDmn":null,"isChnRlt":false,"teachingMode":"F2F","subjGrp":"B02C","noDrop":true},{"subjCode":"SEHH1016","subjTtl":"INTRODUCTION TO INTERNET TECHNOLOGY","subjType":"G","cpulOrEle":"E","cr":3,"geDmn":"Cluster D","isChnRlt":false,"teachingMode":"Blended","subjGrp":"B01A","noDrop":false}]}

let confirmAddDrop = "https://www48.polyu.edu.hk/myhkcc_new/me/addDrop/confirmAddDrop"

const axios = require('axios');

// Create a cookie string
const cookies = '';

setInterval(() => {
  axios.post(addDropVacy, data, {
      headers: {
          'Content-Type': 'application/json', // Specify content type
          'Cookie': cookies // Manually add the Cookie header
      }
  })
  .then(response => {
    let {data} = response
    let hasVcySubj = data.filter(x => x["subjGrpVacys"].filter(z => z["vacy"] > 0).length > 0)
          let grp = hasVcySubj.map(item => item.subjCode);
      console.log('vacy:'+ grp);
    // let subjData = data.filter(x => x["subjCode"] == "BHMH2002")[0]
    // let vacyData = subjData["subjGrpVacys"].filter(x => x["vacy"] > 0)
    // if (vacyData.length > 0) {
    //   let grp = vacyData.map(item => item.subjGrp);
    //   console.log('vacy:' + grp);
    // }
  })
  .catch(error => {
      console.error('Error:', error);
  });
}, 500);

// axios.post(verifyAddDrop, aaa, {
//   headers: {
//       'Content-Type': 'application/json', // Specify content type
//       'Cookie': cookies // Manually add the Cookie header
//   }
// })
// .then(response => {
//   console.log('Success:', response.data);
// })
// .catch(error => {
//   console.error('Error:', error);
// });