import {
    Stitch,
    RemoteMongoClient,
    AnonymousCredential
} from "mongodb-stitch-browser-sdk";

const client = Stitch.initializeDefaultAppClient('dopenotes-psyvy');

const db = client.getServiceClient(RemoteMongoClient.factory, 'mongodb-atlas').db('Notes');

client.auth.loginWithCredential(new AnonymousCredential()).then(user =>
  db.collection('Videos').updateOne({owner_id: client.auth.user.id}, {$set:{number:42}}, {upsert:true})
).then(() =>
  db.collection('Videos').find({owner_id: client.auth.user.id}, { limit: 100}).asArray()
).then(docs => {
    console.log("Found docs", docs)
    console.log("[MongoDB Stitch] Connected to Stitch")
}).catch(err => {
    console.error(err)
});
