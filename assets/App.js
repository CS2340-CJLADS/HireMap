import React, { useEffect, useMemo, useRef, useState } from "react";
import {
  BrowserRouter,
  Routes,
  Route,
  Link,
  useParams,
  Navigate,
  useLocation,
} from "react-router-dom";

/* ---------- Shared shell ---------- */
function Shell({ children }) {
  return (
    <>
      <Header />
      <main>{children}</main>
      <Footer />
    </>
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
        <a href="/admin/" className="btn secondary">Admin</a>
      </nav>
    </header>
  );
}
function Footer() {
  return (
    <footer className="container footer">
      <small>© {new Date().getFullYear()} HireMap — React front-end; data from Django Admin via /api/.</small>
    </footer>
  );
}
function Badge({ children }) { return <span className="badge">{children}</span>; }
function Button({ variant="primary", ...props }) {
  let c = "btn";
  if (variant==="secondary") c += " secondary";
  if (variant==="danger") c += " danger";
  return <button {...props} className={c} />;
}
function Card({ children }) { return <article className="card">{children}</article>; }

/* ---------- Home ---------- */
function HomePage() {
  return (
    <Shell>
      <section className="hero">
        <div className="container">
          <h1>Your Launchpad to the Future</h1>
          <p className="lede">We take care of the hard parts of your job search so you can focus on building your path to success.</p>
          <div className="hero-cta">
            <Link to="/jobs/" className="btn">Get Started</Link>
            <a href="#" className="btn secondary">Log In</a>
          </div>
          <div className="hero-illustration" />
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

      <section className="section">
        <div className="container grid-3">
          <div className="tile"><div><h3>Roadmap Builder</h3><p>Plan goals and milestones so your path is clear and organized.</p></div></div>
          <div className="tile"><div><h3>Extracurriculars</h3><p>Discover curated programs tailored to your passions.</p></div></div>
          <div className="tile"><div><h3>Jobs Near You</h3><p>Explore openings on an interactive map.</p></div></div>
        </div>
      </section>
    </Shell>
  );
}

/* ---------- Jobs List (fetch from /api/jobs/) ---------- */
function useQuery() {
  const { search } = useLocation();
  return React.useMemo(() => new URLSearchParams(search), [search]);
}

function JobsListPage() {
  const params = useQuery();
  const [query, setQuery] = useState({
    q: params.get("q") || "",
    skills: params.get("skills") || "",
    location: params.get("location") || "",
    work_type: params.get("work_type") || "",
    visa: params.get("visa") || "",
  });
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [applyOpen, setApplyOpen] = useState(false);

  useEffect(() => {
    setLoading(true);
    // Simple fetch; you can later expand filters server-side
    fetch("/api/jobs/")
      .then(r => r.ok ? r.json() : Promise.reject(r))
      .then(setJobs)
      .catch(() => setJobs([]))
      .finally(() => setLoading(false));
  }, []);

  function saveSearch() {
    const sp = new URLSearchParams(query).toString();
    const saved = JSON.parse(localStorage.getItem("hm:savedSearches") || "[]");
    const name = window.prompt("Name this search:", sp || "All jobs");
    if (name) {
      saved.push({ name, query: sp, ts: Date.now() });
      localStorage.setItem("hm:savedSearches", JSON.stringify(saved));
      alert("Saved! View at /saved-searches/");
    }
  }

  return (
    <Shell>
      <section className="container section">
        <h1 className="page-title">Find Jobs</h1>
        <form className="filters" onSubmit={(e)=>e.preventDefault()}>
          <input placeholder="Search by title or company" value={query.q} onChange={e=>setQuery({...query,q:e.target.value})}/>
          <input placeholder="Skills (comma separated)" value={query.skills} onChange={e=>setQuery({...query,skills:e.target.value})}/>
          <input placeholder="Location" value={query.location} onChange={e=>setQuery({...query,location:e.target.value})}/>
          <select value={query.work_type} onChange={e=>setQuery({...query,work_type:e.target.value})}>
            <option value="">Any</option>
            <option value="remote">Remote</option>
            <option value="onsite">On-site</option>
            <option value="hybrid">Hybrid</option>
          </select>
          <select value={query.visa} onChange={e=>setQuery({...query,visa:e.target.value})}>
            <option value="">Visa: Any</option>
            <option value="sponsor">Offers Sponsorship</option>
            <option value="no">No Sponsorship</option>
          </select>
          <Button>Search</Button>
          <Button variant="secondary" type="button" onClick={saveSearch}>Save Search</Button>
        </form>

        {loading && <p className="muted">Loading…</p>}
        {!loading && jobs.length === 0 && (
          <Card><p>No jobs yet. Create some in <a href="/admin/">Django Admin</a>.</p></Card>
        )}
        {!loading && jobs.length > 0 && (
          <div className="jobs-grid">
            {jobs.map(j=>(
              <article className="job-card" key={j.id}>
                <div className="job-card-top">
                  <h3><Link to={`/jobs/${j.id}/`}>{j.title}</Link></h3>
                  <Badge>{j.work_type || "—"}</Badge>
                </div>
                <p className="muted">{j.company}{j.location ? ` — ${j.location}` : ""}</p>
                <p>{j.summary || " "}</p>
                <div className="job-meta">
                  <span>Salary: {j.salary || "—"}</span>
                  <span>Skills: {j.skills || "—"}</span>
                </div>
                <div className="job-actions">
                  <Link className="btn" to={`/jobs/${j.id}/`}>View</Link>
                  <Button variant="secondary" onClick={()=>setApplyOpen(true)}>Quick Apply</Button>
                </div>
              </article>
            ))}
          </div>
        )}
      </section>

      {applyOpen && (
        <Modal title="Apply with One Click" onClose={()=>setApplyOpen(false)}>
          <p className="muted">Attach your default resume and add an optional tailored note.</p>
          <label className="label">Note to recruiter (optional)</label>
          <textarea rows={5} placeholder="Briefly explain why you're a great fit…"/>
          <label className="checkbox"><input type="checkbox" defaultChecked/> Use default resume on file</label>
          <div className="modal-actions">
            <Button onClick={()=>{alert("Sent (demo)."); setApplyOpen(false);}}>Send Application</Button>
            <Button variant="secondary" onClick={()=>setApplyOpen(false)}>Cancel</Button>
          </div>
        </Modal>
      )}
    </Shell>
  );
}

function Modal({ title, onClose, children }) {
  useEffect(() => {
    const onEsc = e => e.key === "Escape" && onClose();
    window.addEventListener("keydown", onEsc);
    return () => window.removeEventListener("keydown", onEsc);
  }, [onClose]);
  return (
    <div className="modal" role="dialog" aria-modal="true">
      <div className="modal-dialog">
        <button className="modal-close" onClick={onClose}>&times;</button>
        <h3>{title}</h3>
        {children}
      </div>
    </div>
  );
}

/* ---------- Job Detail (fetch /api/jobs/:pk/) ---------- */
function JobDetailPage() {
  const { pk } = useParams();
  const [job, setJob] = useState(null);
  const [open, setOpen] = useState(false);

  useEffect(() => {
    fetch(`/api/jobs/${pk}/`)
      .then(r => r.ok ? r.json() : Promise.reject(r))
      .then(setJob)
      .catch(()=>setJob(null));
  }, [pk]);

  return (
    <Shell>
      <section className="container section">
        <Link to="/jobs/" className="link-back">← Back to Jobs</Link>
        {!job && <Card><p>That job isn’t available. Try the <Link to="/jobs/">jobs list</Link>.</p></Card>}

        {job && (
          <>
            <header className="job-header">
              <h1>{job.title}</h1>
              <div>
                <Badge>{job.work_type || "—"}</Badge>
                <Button variant="secondary" onClick={()=>{
                  const saved = JSON.parse(localStorage.getItem("hm:savedJobs")||"[]");
                  saved.push({ id: job.id, title: job.title, company: job.company });
                  localStorage.setItem("hm:savedJobs", JSON.stringify(saved));
                  alert("Saved (demo).");
                }}>Save</Button>
                <Button onClick={()=>setOpen(true)}>Apply</Button>
              </div>
            </header>
            <p className="muted">
              {job.company}{job.location ? ` — ${job.location}` : ""}{job.salary ? ` • ${job.salary}` : ""}{job.skills ? ` • ${job.skills}` : ""}
            </p>
            <Card>
              <h3>About the role</h3>
              <p>{job.description || job.summary || " "}</p>
              {job.responsibilities?.length ? (<><h3>Responsibilities</h3><ul className="list">{job.responsibilities.map((r,i)=><li key={i}>{r}</li>)}</ul></>) : null}
              {job.qualifications?.length ? (<><h3>Qualifications</h3><ul className="list">{job.qualifications.map((q,i)=><li key={i}>{q}</li>)}</ul></>) : null}
            </Card>
          </>
        )}
      </section>

      {open && (
        <Modal title={`Apply to ${job?.title || "this job"}`} onClose={()=>setOpen(false)}>
          <p className="muted">One-click apply with an optional tailored note.</p>
          <label className="label">Note to recruiter (optional)</label>
          <textarea rows={5} placeholder="Why you’re a match…"/>
          <label className="checkbox"><input type="checkbox" defaultChecked/> Use default resume on file</label>
          <div className="modal-actions">
            <Button onClick={()=>{alert("Sent (demo)."); setOpen(false);}}>Send Application</Button>
            <Button variant="secondary" onClick={()=>setOpen(false)}>Cancel</Button>
          </div>
        </Modal>
      )}
    </Shell>
  );
}

/* ---------- Applications (UI only for now) ---------- */
function ApplicationsBoardPage() {
  const [cols] = useState([
    { key: "applied", title: "Applied", cards: [] },
    { key: "review", title: "Review", cards: [] },
    { key: "interview", title: "Interview", cards: [] },
    { key: "offer", title: "Offer", cards: [] },
    { key: "closed", title: "Closed", cards: [] },
  ]);
  return (
    <Shell>
      <section className="container section">
        <h1 className="page-title">Application Tracker</h1>
        <div className="kanban">
          {cols.map(col=>(
            <div key={col.key} className="kanban-col">
              <div className="kanban-col-head">{col.title}</div>
              <div className="kanban-col-body">
                {col.cards.length === 0 && <Card><p>No applications in this stage yet.</p></Card>}
              </div>
            </div>
          ))}
        </div>
        <p className="muted small">Wire to real data later if needed.</p>
      </section>
    </Shell>
  );
}

/* ---------- Profile / Recruiter / Messages (UI placeholders; no seeded data) ---------- */
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
        <Card><p>No job posts yet. Create your first job in <a href="/admin/">Admin</a> or build a form/API later.</p></Card>
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
          <label className="label">Location</label>
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

/* ---------- Map (fetch /api/jobs/?has_location=true) ---------- */
function MapPage() {
  const mapRef = useRef(null);
  useEffect(()=>{
    if (!window.L || mapRef.current) return;
    const map = window.L.map("leaflet-map").setView([33.7490, -84.3880], 12);
    mapRef.current = map;
    window.L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", { maxZoom: 19, attribution: "&copy; OpenStreetMap" }).addTo(map);

    fetch("/api/jobs/?has_location=true")
      .then(r=>r.ok?r.json():Promise.reject(r))
      .then(list=>{
        list.forEach(j=>{
          if (j.lat != null && j.lng != null) {
            const m = window.L.marker([j.lat, j.lng]).addTo(map);
            m.bindPopup(`<strong>${j.title}</strong><br/>${j.company ?? ""}`);
          }
        });
      })
      .catch(()=>{});
  },[]);

  return (
    <Shell>
      <section className="container section">
        <h1 className="page-title">Jobs Near You</h1>
        <p className="muted">Add latitude/longitude to job records in Admin to see markers.</p>
        <div id="leaflet-map" className="map" />
      </section>
    </Shell>
  );
}

/* ---------- Router ---------- */
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
        <Route path="/saved-searches/" element={<SavedSearchesPage/>} />
        <Route path="/messages/" element={<MessagesPage/>} />
        <Route path="/map/" element={<MapPage/>} />
        <Route path="*" element={<Navigate to="/" replace/>} />
      </Routes>
    </BrowserRouter>
  );
}

/* ---------- Saved Searches (localStorage only) ---------- */
function SavedSearchesPage() {
  const [saved, setSaved] = useState([]);
  useEffect(()=>{ setSaved(JSON.parse(localStorage.getItem("hm:savedSearches") || "[]")); },[]);
  function del(ts){
    const next = saved.filter(s=>String(s.ts)!==String(ts));
    localStorage.setItem("hm:savedSearches", JSON.stringify(next));
    setSaved(next);
  }
  return (
    <Shell>
      <section className="container section">
        <h1 className="page-title">Saved Searches</h1>
        <div className="grid-3">
          {saved.length===0 ? <Card><p>No saved searches yet.</p></Card> :
            saved.map(s=>(
              <Card key={s.ts}>
                <h3>{s.name}</h3>
                <p className="muted">{new Date(s.ts).toLocaleString()}</p>
                <div className="job-actions">
                  <Link className="btn" to={`/jobs/?${s.query}`}>Run</Link>
                  <Button variant="secondary" onClick={()=>del(s.ts)}>Delete</Button>
                </div>
              </Card>
            ))}
        </div>
      </section>
    </Shell>
  );
}
