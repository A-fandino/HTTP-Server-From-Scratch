console.log("The script loaded!!!")

const printApi = async () => {
    const resp = await fetch("/static/a.json")
    console.log(await resp.json())
}

printApi()