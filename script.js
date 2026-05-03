let currentUser = "";

function getBrowser(){
    const ua = navigator.userAgent;
    if(ua.includes("Edg")) return "Edge";
    if(ua.includes("Firefox")) return "Firefox";
    if(ua.includes("Chrome") && !ua.includes("Edg")) return "Chrome";
    return "Unknown";
}

async function login(){
    const u = document.getElementById("u").value;
    const p = document.getElementById("p").value;

    const res = await fetch("http://127.0.0.1:8000/login",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({username:u,password:p})
    });

    const data = await res.json();
    if(data.status==="success"){
        localStorage.setItem("user",u);
        window.location="employee.html";
    } else alert("Invalid Login");
}

async function access(){
    const file = document.getElementById("file").value;
    const size = document.getElementById("size").value;
    const user = localStorage.getItem("user");

    
    const ipRes = await fetch("https://api.ipify.org?format=json");
    const ipData = await ipRes.json();

    await fetch("http://127.0.0.1:8000/log",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({
            username:user,
            file_name:file,
            file_size:parseInt(size),
            ip:ipData.ip,
            browser:getBrowser()
        })
    });

    alert("File access logged!");
}

async function loadHR(){
    const res = await fetch("http://127.0.0.1:8000/hr-logs");
    const data = await res.json();

    let t = `<tr>
        <th>User</th><th>File</th><th>Size</th>
        <th>IP</th><th>Browser</th><th>Time</th>
        <th>Status</th><th>Reason</th></tr>`;

   data.forEach(r=>{
    const rowClass = r.suspicious ? "suspicious" : "safe";

    t += `<tr class="${rowClass}">
        <td>${r.username}</td>
        <td>${r.file_name}</td>
        <td>${r.file_size}</td>
        <td>${r.ip}</td>
        <td>${r.browser}</td>
        <td>${r.time}</td>
        <td>${r.suspicious ? "Suspicious" : "Safe"}</td>
        <td>${r.reason}</td>
    </tr>`;
});
    document.getElementById("hrTable").innerHTML=t;
}

async function clearLogs(){
    await fetch("http://127.0.0.1:8000/clear",{method:"DELETE"});
    loadHR();
}
