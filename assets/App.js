import React, { useEffect, useMemo, useRef, useState } from "react";
import {
  BrowserRouter,
  Routes,
  Route,
  Link,
  Navigate,
  useParams,
  useLocation,
  useNavigate,
} from "react-router-dom";

/* =========================================================================
   Data loading (front-end only; no backend changes required)
   ========================================================================= */

const JOBS_URLS_TRY = [
  "/api/jobs/",
  "/jobs/data/",
  "/jobs/json/",
  "/jobs/list/",
];

function getInitialJobsFromDOM() {
  // If your backend injects jobs as JSON into the page:
  const el = document.getElementById("jobs-data");
  if (!el) return null;
  try {
    const parsed = JSON.parse(el.textContent || "null");
    if (Array.isArray(parsed)) return parsed;
  } catch {}
  return null;
}

async function tryLoadJobsFromServer() {
  for (const url of JOBS_URLS_TRY) {
    try {
      const res = await fetch(url, { credentials: "same-origin" });
      if (!res.ok) continue;
      const data = await res.json();
      if (Array.isArray(data)) return data;
    } catch {}
  }
  return [];
}

/* =========================================================================
   Auth state (front-end only)
   - If backend injects <script id="auth-user">{"name": "...", "avatar": "..."}</script>
     we’ll show that avatar and link to /profile/.
   - Otherwise, we show a default avatar and link to /accounts/login/.
   ========================================================================= */
function getAuthUserFromDOM() {
  const el = document.getElementById("auth-user");
  if (!el) return null;
  try {
    const parsed = JSON.parse(el.textContent || "null");
    if (parsed && typeof parsed === "object") return parsed;
  } catch {}
  return null;
}

/* =========================================================================
   Geocoding (address -> coords) using Nominatim; cached in localStorage
   ========================================================================= */
async function geocodeAddress(address) {
  const key = `hm:geocode:${address}`;
  const cached = localStorage.getItem(key);
  if (cached) {
    try { return JSON.parse(cached); } catch {}
  }
  const url = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(address)}&limit=1`;
  try {
    const res = await fetch(url);
    if (!res.ok) return null;
    const data = await res.json();
    if (Array.isArray(data) && data.length > 0) {
      const { lat, lon } = data[0];
      const result = { lat: parseFloat(lat), lng: parseFloat(lon) };
      localStorage.setItem(key, JSON.stringify(result));
      await new Promise(r => setTimeout(r, 200)); // polite throttle
      return result;
    }
  } catch {}
  return null;
}

/* =========================================================================
   Layout
   ========================================================================= */
function Shell({ children }) {
  return (
    <>
      <Header />
      <main>{children}</main>
      <Footer />
    </>
  );
}

function AvatarButton() {
  const navigate = useNavigate();
  const user = getAuthUserFromDOM(); // { name, avatar } or null
  const isAuthed = !!user;

  const onClick = () => {
    if (isAuthed) navigate("/profile/");
    else navigate("/accounts/login/"); // change to your sign-up/login as needed
  };

  // default placeholder avatar (SVG)
  const fallback =
    "data:image/svg+xml;utf8," +
    encodeURIComponent(
      `<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'>
        <circle cx='32' cy='24' r='14' fill='#dfeeea' stroke='#2a6f6a' stroke-width='2'/>
        <path d='M8 58c4-12 16-18 24-18s20 6 24 18' fill='#dfeeea' stroke='#2a6f6a' stroke-width='2'/>
      </svg>`
    );

  return (
    <button className="avatar-btn" onClick={onClick} title={isAuthed ? "Your profile" : "Sign in / Create account"}>
      <img
        className="avatar"
        src={(user && user.avatar) || fallback}
        alt={isAuthed ? (user.name || "Account") : "Sign in"}
        referrerPolicy="no-referrer"
      />
    </button>
  );
}

function Header() {
  return (
    <header className="container nav">
      <Link to="/" className="brand">HireMap</Link>
      <nav className="nav-actions">
        <Link to="/jobs/">Jobs</Link>
        <Link to="/applications/">Applications</Link>
        <Link to="/map/">Map</Link>
        <Link to="/recruiter/jobs/">Recruiter</Link>
        <Link to="/profile/">Profile</Link>
        <Link to="/messages/">Messages</Link>
        {/* Removed Admin button per request */}
        <AvatarButton />
      </nav>
    </header>
  );
}

function Footer() {
  return (
    <footer className="container footer">
      <small>© {new Date().getFullYear()} HireMap — React front end; backend/Admin remain as in your archive.</small>
    </footer>
  );
}

function Button({ variant="primary", ...props }) {
  let c = "btn";
  if (variant==="secondary") c += " secondary";
  if (variant==="danger") c += " danger";
  return <button {...props} className={c} />;
}
function Card({ children }) { return <article className="card">{children}</article>; }
function Badge({ children }) { return <span className="badge">{children}</span>; }

/* =========================================================================
   Home with Mini Map centered between “Log in” and “Create account”
   ========================================================================= */
function HomeMiniMap({ jobs }) {
  const mapRef = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (!window.L || mapRef.current) return;
    const map = window.L.map("home-mini-map", {
      zoomControl: false,
      attributionControl: false,
      scrollWheelZoom: false,
      dragging: true,
    }).setView([33.7490, -84.3880], 11);
    mapRef.current = map;
    window.L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", { maxZoom: 19 }).addTo(map);
  }, []);

  useEffect(() => {
    (async () => {
      if (!jobs || !mapRef.current || !window.L) return;
      const subset = jobs.slice(0, 20);
      for (const j of subset) {
        const addr = j.location || j.address;
        if (!addr) continue;
        const coords = await geocodeAddress(addr);
        if (!coords) continue;
        const m = window.L.marker([coords.lat, coords.lng]).addTo(mapRef.current);
        m.bindPopup(`<strong>${j.title ?? "Job"}</strong><br/>${j.company ?? ""}<br/>${addr}`);
      }
    })();
  }, [jobs]);

  return (
    <div
      id="home-mini-map"
      className="mini-map"
      role="button"
      title="Open full map"
      onClick={() => navigate("/map/")}
    >
      <div className="mini-map-overlay">Open Map</div>
    </div>
  );
}

function HomePage() {
  const [jobs, setJobs] = useState(null);

  useEffect(() => {
    const injected = getInitialJobsFromDOM();
    if (injected) { setJobs(injected); return; }
    (async () => setJobs(await tryLoadJobsFromServer()))();
  }, []);

  return (
    <Shell>
      <section className="hero">
        <div className="container">
          <h1>Your Launchpad to the Future</h1>
          <p className="lede">We take care of the hard parts of your job search so you can focus on building your path to success.</p>

          {/* Tri-column strip: Login | Mini Map | Create Account */}
          <div className="hero-triad">
            <Card>
              <h3>Welcome back</h3>
              <p className="muted">Already have an account?</p>
              <Link to="/accounts/login/" className="btn">Log In</Link>
            </Card>

            <HomeMiniMap jobs={jobs || []} />

            <Card>
              <h3>New here?</h3>
              <p className="muted">Create a free account to get started.</p>
              <Link to="/accounts/register/" className="btn secondary">Create Account</Link>
            </Card>
          </div>

          <div className="pills"><span>Find Jobs Faster</span><span>Boost Application Tracking</span></div>
        </div>
      </section>

      <section className="section">
        <div className="container grid-3">
          <Card><h3>Scholarship Help</h3><p>Connect funding to opportunity.</p></Card>
          <Card><h3>College Applications</h3><p>Keep essays, deadlines, and lists in one dashboard.</p></Card>
          <Card><h3>Test Prep</h3><p>Track practice scores and improve steadily.</p></Card>
        </div>
      </section>
    </Shell>
  );
}

/* =========================================================================
   Jobs (front-end only; no hard-coded entries)
   ========================================================================= */
function useQuery() {
  const { search } = useLocation();
  return useMemo(() => new URLSearchParams(search), [search]);
}

function JobsListPage() {
  const params = useQuery();
  const [filters, setFilters] = useState({
    q: params.get("q") || "",
    skills: params.get("skills") || "",
    location: params.get("location") || "",
    work_type: params.get("work_type") || "",
  });
  const [jobs, setJobs] = useState(null);

  useEffect(() => {
    const injected = getInitialJobsFromDOM();
    if (injected) { setJobs(injected); return; }
    (async () => setJobs(await tryLoadJobsFromServer()))();
  }, []);

  const list = (jobs || []).filter(j => {
    const q = filters.q.trim().toLowerCase();
    const s = filters.skills.trim().toLowerCase();
    const loc = filters.location.trim().toLowerCase();
    const wt = filters.work_type.trim().toLowerCase();
    const hay = `${j.title ?? ""} ${j.company ?? ""} ${j.summary ?? ""} ${j.description ?? ""}`.toLowerCase();
    const skills = `${j.skills ?? ""}`.toLowerCase();
    const jLoc = `${j.location ?? j.address ?? ""}`.toLowerCase();
    const jWT = `${j.work_type ?? ""}`.toLowerCase();
    return (!q || hay.includes(q))
        && (!s || skills.includes(s))
        && (!loc || jLoc.includes(loc))
        && (!wt || jWT === wt);
  });

  return (
    <Shell>
      <section className="container section">
        <h1 className="page-title">Find Jobs</h1>

        <form className="filters" onSubmit={(e)=>e.preventDefault()}>
          <input placeholder="Search" value={filters.q} onChange={e=>setFilters({...filters,q:e.target.value})}/>
          <input placeholder="Skills (comma separated)" value={filters.skills} onChange={e=>setFilters({...filters,skills:e.target.value})}/>
          <input placeholder="Location" value={filters.location} onChange={e=>setFilters({...filters,location:e.target.value})}/>
          <select value={filters.work_type} onChange={e=>setFilters({...filters,work_type:e.target.value})}>
            <option value="">Any</option>
            <option value="remote">Remote</option>
            <option value="onsite">On-site</option>
            <option value="hybrid">Hybrid</option>
          </select>
          <Button>Search</Button>
        </form>

        {jobs === null && <p className="muted">Loading…</p>}
        {jobs && list.length === 0 && (
          <Card><p>No jobs to show yet. Once your backend provides data (via injected JSON or an existing JSON endpoint), they’ll appear here automatically.</p></Card>
        )}
        {jobs && list.length > 0 && (
          <div className="jobs-grid">
            {list.map((j, idx) => (
              <article className="job-card" key={j.id ?? `${idx}-${j.title}-${j.company}`}>
                <div className="job-card-top">
                  <h3><Link to={`/jobs/${j.id ?? ""}`}>{j.title}</Link></h3>
                  <Badge>{j.work_type || "—"}</Badge>
                </div>
                <p className="muted">{[j.company, j.location || j.address].filter(Boolean).join(" — ")}</p>
                <p>{j.summary || j.description || ""}</p>
                <div className="job-meta">
                  <span>Salary: {j.salary || "—"}</span>
                  <span>Skills: {j.skills || "—"}</span>
                </div>
                <div className="job-actions">
                  <Link className="btn" to={`/jobs/${j.id ?? ""}`}>View</Link>
                </div>
              </article>
            ))}
          </div>
        )}
      </section>
    </Shell>
  );
}

function JobDetailPage() {
  const { pk } = useParams();
  const [job, setJob] = useState(null);
  const [status, setStatus] = useState("loading"); // loading | empty | ok

  useEffect(() => {
    const injected = getInitialJobsFromDOM();
    if (injected && pk) {
      const match = injected.find(j => String(j.id) === String(pk));
      if (match) { setJob(match); setStatus("ok"); return; }
    }
    setStatus("empty"); // no detail endpoint used here
  }, [pk]);

  return (
    <Shell>
      <section className="container section">
        <Link to="/jobs/" className="link-back">← Back to Jobs</Link>
        {status === "loading" && <p className="muted">Loading…</p>}
        {status === "empty" && <Card><p>That job isn’t available yet. Once the backend exposes it, this page will populate automatically.</p></Card>}
        {status === "ok" && job && (
          <>
            <header className="job-header">
              <h1>{job.title}</h1>
              <Badge>{job.work_type || "—"}</Badge>
            </header>
            <p className="muted">{[job.company, job.location || job.address, job.salary].filter(Boolean).join(" • ")}</p>
            <Card>
              <h3>About the role</h3>
              <p>{job.description || job.summary || ""}</p>
              {Array.isArray(job.responsibilities) && job.responsibilities.length > 0 && (
                <>
                  <h3>Responsibilities</h3>
                  <ul className="list">{job.responsibilities.map((r,i)=><li key={i}>{r}</li>)}</ul>
                </>
              )}
              {Array.isArray(job.qualifications) && job.qualifications.length > 0 && (
                <>
                  <h3>Qualifications</h3>
                  <ul className="list">{job.qualifications.map((q,i)=><li key={i}>{q}</li>)}</ul>
                </>
              )}
            </Card>
          </>
        )}
      </section>
    </Shell>
  );
}

/* =========================================================================
   Applications / Profile / Recruiter / Messages — UI only
   ========================================================================= */
function ApplicationsBoardPage() {
  const cols = [
    { key: "applied", title: "Applied" },
    { key: "review", title: "Review" },
    { key: "interview", title: "Interview" },
    { key: "offer", title: "Offer" },
    { key: "closed", title: "Closed" },
  ];
  return (
    <Shell>
      <section className="container section">
        <h1 className="page-title">Application Tracker</h1>
        <div className="kanban">
          {cols.map(col=>(
            <div key={col.key} className="kanban-col">
              <div className="kanban-col-head">{col.title}</div>
              <div className="kanban-col-body">
                <Card><p>No applications in this stage yet.</p></Card>
              </div>
            </div>
          ))}
        </div>
      </section>
    </Shell>
  );
}

function ProfilePage() {
  return (
    <Shell>
      <section className="container section">
        <h1 className="page-title">Your Profile</h1>
        <div className="grid-2">
          <form className="card form" onSubmit={(e)=>e.preventDefault()}>
            <h3>Basics</h3>
            <label className="label">Headline</label>
            <input type="text" placeholder=""/>
            <label className="label">Location</label>
            <input type="text" placeholder=""/>
            <label className="label">Links</label>
            <input type="url" placeholder=""/>
            <input type="url" placeholder=""/>
            <div className="form-actions">
              <Button type="button">Save Changes</Button>
              <Button variant="secondary" type="reset">Reset</Button>
            </div>
          </form>

          <form className="card form" onSubmit={(e)=>e.preventDefault()}>
            <h3>Skills</h3>
            <label className="label">Add skills (comma separated)</label>
            <input type="text" placeholder=""/>
            <h3>Education</h3>
            <input type="text" placeholder=""/>
            <h3>Work Experience</h3>
            <textarea rows={5} placeholder=""/>
            <div className="form-actions">
              <Button type="button">Save Section</Button>
            </div>
          </form>
        </div>
      </section>
    </Shell>
  );
}

function RecruiterJobsPage() {
  return (
    <Shell>
      <section className="container section">
        <div className="page-head">
          <h1 className="page-title">Your Job Posts</h1>
          <Link to="/recruiter/jobs/new/" className="btn">Post a Job</Link>
        </div>
        <Card><p>This UI is ready. When your backend exposes endpoints, this page will use them with no hard-coded entries.</p></Card>
      </section>
    </Shell>
  );
}

function RecruiterJobFormPage() {
  return (
    <Shell>
      <section className="container section">
        <h1 className="page-title">Post a Job</h1>
        <form className="card form" onSubmit={(e)=>e.preventDefault()}>
          <label className="label">Job Title</label>
          <input type="text" placeholder=""/>
          <label className="label">Company</label>
          <input type="text" placeholder=""/>
          <label className="label">Location (Address)</label>
          <input type="text" placeholder=""/>
          <label className="label">Work Type</label>
          <select><option>Remote</option><option>On-site</option><option>Hybrid</option></select>
          <label className="label">Salary Range</label>
          <input type="text" placeholder=""/>
          <label className="label">Skills</label>
          <input type="text" placeholder=""/>
          <label className="label">Description</label>
          <textarea rows={8} placeholder=""/>
          <div className="form-actions">
            <Button type="button">Save Draft</Button>
            <Button variant="secondary" type="button">Publish</Button>
          </div>
        </form>
      </section>
    </Shell>
  );
}

function MessagesPage() {
  return (
    <Shell>
      <section className="container section">
        <h1 className="page-title">Messages</h1>
        <Card><p>No messages yet.</p></Card>
      </section>
    </Shell>
  );
}

/* =========================================================================
   Full Map — address-based markers
   ========================================================================= */
function MapPage() {
  const mapRef = useRef(null);
  const [jobs, setJobs] = useState(null);

  useEffect(() => {
    const injected = getInitialJobsFromDOM();
    if (injected) { setJobs(injected); return; }
    (async () => setJobs(await tryLoadJobsFromServer()))();
  }, []);

  useEffect(() => {
    if (!window.L || mapRef.current) return;
    const map = window.L.map("leaflet-map").setView([33.7490, -84.3880], 12);
    mapRef.current = map;
    window.L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19, attribution: "&copy; OpenStreetMap"
    }).addTo(map);
  }, []);

  useEffect(() => {
    (async () => {
      if (!jobs || !mapRef.current || !window.L) return;
      for (const j of jobs) {
        const addr = j.location || j.address;
        if (!addr) continue;
        const coords = await geocodeAddress(addr);
        if (!coords) continue;
        const m = window.L.marker([coords.lat, coords.lng]).addTo(mapRef.current);
        m.bindPopup(`<strong>${j.title ?? "Job"}</strong><br/>${j.company ?? ""}<br/>${addr}`);
      }
    })();
  }, [jobs]);

  return (
    <Shell>
      <section className="container section">
        <h1 className="page-title">Jobs Near You</h1>
        <p className="muted">Markers are based on each job’s <strong>address</strong> (not lat/lng). We geocode in the browser and cache results locally.</p>
        <div id="leaflet-map" className="map" />
      </section>
    </Shell>
  );
}

/* =========================================================================
   Router
   ========================================================================= */
export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage/>} />
        <Route path="/jobs/" element={<JobsListPage/>} />
        <Route path="/jobs/:pk/" element={<JobDetailPage/>} />
        <Route path="/applications/" element={<ApplicationsBoardPage/>} />
        <Route path="/profile/" element={<ProfilePage/>} />
        <Route path="/recruiter/jobs/" element={<RecruiterJobsPage/>} />
        <Route path="/recruiter/jobs/new/" element={<RecruiterJobFormPage/>} />
        <Route path="/messages/" element={<MessagesPage/>} />
        <Route path="/map/" element={<MapPage/>} />
        <Route path="*" element={<Navigate to="/" replace/>} />
      </Routes>
    </BrowserRouter>
  );
}
