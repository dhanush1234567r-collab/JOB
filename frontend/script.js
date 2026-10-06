let allJobs = [];
let currentJob = null;

fetch("/api/jobs")
  .then(r => r.json())
  .then(jobs => {
    allJobs = jobs;
    fill("location", [...new Set(jobs.map(j => j.location))].sort());
    fill("type", [...new Set(jobs.map(j => j.type))].sort());
    render();
  })
  .catch(() => document.getElementById("jobs").innerText = "Failed to load jobs");

function fill(id, values) {
  const sel = document.getElementById(id);
  values.forEach(v => sel.innerHTML += `<option>${v}</option>`);
}

function render() {
  const q = document.getElementById("search").value.toLowerCase();
  const loc = document.getElementById("location").value;
  const type = document.getElementById("type").value;
  const list = allJobs.filter(j =>
    (!q || (j.title + j.company).toLowerCase().includes(q)) &&
    (!loc || j.location === loc) && (!type || j.type === type));
  document.getElementById("jobs").innerHTML = list.length ? list.map(j => `
    <div class="job">
      <h3>${j.title}</h3>
      <p class="company">${j.company}</p>
      <p class="location">&#128205; ${j.location}</p>
      <p class="salary">${j.type} | ${j.salary}</p>
      <button onclick="openModal(${j.id})">Apply Now</button>
    </div>`).join("") : "<p>No jobs found</p>";
}

function openModal(id) {
  currentJob = allJobs.find(j => j.id === id);
  document.getElementById("modal-title").innerText = `Apply for ${currentJob.title}`;
  showMsg("", true);
  document.getElementById("modal").classList.add("show");
}

function closeModal() {
  document.getElementById("modal").classList.remove("show");
}

function showMsg(text, ok) {
  const m = document.getElementById("msg");
  m.innerText = text;
  m.className = "msg " + (ok ? "ok" : "err");
}

function submitApply() {
  const name = document.getElementById("name").value.trim();
  const email = document.getElementById("email").value.trim();
  const phone = document.getElementById("phone").value.trim();
  const cover = document.getElementById("cover").value.trim();
  const resume = document.getElementById("resume").files[0];

  if (!name || !email || !phone) { showMsg("Please fill name, email and phone.", false); return; }
  if (!resume) { showMsg("Please upload your resume.", false); return; }
  if (resume.size > 5 * 1024 * 1024) { showMsg("Resume must be under 5 MB.", false); return; }

  const fd = new FormData();
  fd.append("name", name);
  fd.append("email", email);
  fd.append("phone", phone);
  fd.append("cover_letter", cover);
  fd.append("resume", resume);

  const btn = document.querySelector(".modal-box button.submit");
  btn.disabled = true;
  btn.innerText = "Submitting...";

  fetch("/api/apply/" + currentJob.id, { method: "POST", body: fd })
    .then(r => r.json().then(d => ({ ok: r.ok, d })))
    .then(({ ok, d }) => {
      if (ok) {
        showMsg(`Thanks, ${name}. Your application for ${currentJob.title} has been submitted.`, true);
        ["email", "phone", "cover", "resume"].forEach(i => document.getElementById(i).value = "");
        document.getElementById("name").value = "";
      } else {
        showMsg(d.message, false);
      }
    })
    .catch(() => showMsg("Submit failed. Please try again.", false))
    .finally(() => {
      btn.disabled = false;
      btn.innerText = "Submit application";
    });
}
