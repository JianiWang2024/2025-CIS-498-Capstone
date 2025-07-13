import React, { useState, useEffect } from 'react';

// Lab 2: Set up Node.js and create-react-app for React development
// Simple Router
const Router = ({ children, isLoggedIn, setIsLoggedIn }) => {
  const [currentPath, setCurrentPath] = useState('/');

  // Lab 2: Develop basic JavaScript to manipulate the DOM
  useEffect(() => {
    const handlePopState = () => setCurrentPath(window.location.pathname);
    window.addEventListener('popstate', handlePopState);
    return () => window.removeEventListener('popstate', handlePopState);
  }, []);

  const navigate = (path) => {
    window.history.pushState({}, '', path);
    setCurrentPath(path);
  };

  return (
    <div>
      {React.Children.map(children, (child) =>
        React.cloneElement(child, { currentPath, navigate, isLoggedIn, setIsLoggedIn })
      )}
    </div>
  );
};

const Route = ({ path, component: Component, currentPath, navigate, isLoggedIn, setIsLoggedIn, ...props }) => {
  const protectedPaths = ['/about', '/report', '/items'];

  const isProtected = protectedPaths.includes(path);

  if (isProtected && !isLoggedIn) {
    navigate('/login');
    return null;
  }

  if (currentPath === path) {
    return <Component navigate={navigate} isLoggedIn={isLoggedIn} setIsLoggedIn={setIsLoggedIn} {...props} />;
  }

  return null;
};

// Lab 2: Build a simple React component
const Navigation = ({ navigate, currentPath, isLoggedIn, onLogout }) => (
  <nav className="nav">
    <strong>Lost & Found</strong>
    {['/', '/about', '/report', '/items', '/login'].map((path, i) => (
      <span
        key={path}
        className={currentPath === path ? 'nav-link active' : 'nav-link'}
        onClick={() => navigate(path)}
      >
        {['Home', 'About', 'Report Item', 'All Items', 'Login'][i]}
      </span>
    ))}
    {isLoggedIn && (
      <span className="nav-link" onClick={onLogout}>
        Logout
      </span>
    )}
  </nav>
);

// Lab 3: Set up and structure a React project
// Home Page
const HomePage = ({ navigate, allItems }) => {
  const latestItem = allItems.slice(-1)[0];

  useEffect(() => {
    document.title = 'Lost & Found';
  }, []);

  // Lab 2: Handling events and managing state in a React application
  return (
    <div className="page">
      <h1>Lost & Found</h1>
      <button className="btn-primary" onClick={() => navigate('/report')}>
        Report Item
      </button>

      {latestItem && (
        <div className="item-card">
          <div className="item-header">
            <h3>{latestItem.title}</h3>
            <span className={`badge ${latestItem.type}`}>{latestItem.type}</span>
          </div>
          <p>{latestItem.type === 'found' ? 'Found at' : 'Lost in'} {latestItem.location}</p>
          <p className="date">{latestItem.date}</p>
        </div>
      )}
    </div>
  );
};

// Report Page
const ReportPage = ({ navigate, onAddItem }) => {
  const [formData, setFormData] = useState({
    type: '', title: '', address: '', city: '', zipCode: '', description: '', email: ''
  });
  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  
// Lab 3: Build a Todo List application in React and
// demonstrate API usage — Since I haven't implemented a backend yet,
// the "Fetch data from APIs using Axios or Fetch API" step is temporarily not completed.
// I focused on building the front-end features first, including the Todo-like report list
// using React state. Once the backend is ready, I plan to integrate API calls accordingly.

  const [submittedReports, setSubmittedReports] = useState([]);
  
  useEffect(() => { document.title = 'Report Item - Lost & Found'; }, []);
  
  const validateForm = () => {
    const newErrors = {};
    if (!formData.type) newErrors.type = 'Please select item type';
    if (!formData.title.trim()) newErrors.title = 'Please enter item title';
    if (!formData.address.trim()) newErrors.address = 'Please enter address';
    if (!formData.city.trim()) newErrors.city = 'Please enter city';
    if (!/^\d{5}$/.test(formData.zipCode)) newErrors.zipCode = 'Please enter valid 5-digit ZIP code';
    if (!formData.description.trim()) newErrors.description = 'Please enter description';
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) newErrors.email = 'Please enter valid email';
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validateForm()) return;
    
    setIsSubmitting(true);
    setTimeout(() => {
      // To build new items
      const newItem = {
        id: Date.now(),
        title: formData.title,
        location: `${formData.address}, ${formData.city} ${formData.zipCode}`,
        date: new Date().toLocaleDateString('en-US', { month: 'long', day: 'numeric' }),
        type: formData.type,
        description: formData.description,
        email: formData.email,
        submittedAt: new Date().toLocaleString()
      };
      
      onAddItem(newItem);
      
      const reportRecord = {
        id: Date.now() + 1,
        ...formData,
        submittedAt: new Date().toLocaleString()
      };
      setSubmittedReports(prev => [...prev, reportRecord]);
      
      alert(`Thank you! Your ${formData.type} item "${formData.title}" has been submitted and will appear in the All Items page.`);
      setIsSubmitting(false);
      setFormData({ type: '', title: '', address: '', city: '', zipCode: '', description: '', email: '' });
    }, 1000);
  };
  
  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    if (errors[field]) setErrors(prev => ({ ...prev, [field]: '' }));
  };
  
  return (
    <div className="page">
      <h1>Report Lost or Found Item</h1>
      
      <div className="form">
        <div className="form-group">
          <select
            className={errors.type ? 'form-control error' : 'form-control'}
            value={formData.type}
            onChange={(e) => handleChange('type', e.target.value)}
          >
            <option value="">Select Type</option>
            <option value="lost">Lost</option>
            <option value="found">Found</option>
          </select>
          {errors.type && <div className="error-msg">{errors.type}</div>}
        </div>
        
        {[
          { field: 'title', placeholder: 'Item title (e.g., Black Umbrella)', type: 'text' },
          { field: 'address', placeholder: 'Street Address', type: 'text' },
          { field: 'city', placeholder: 'City', type: 'text' },
          { field: 'zipCode', placeholder: 'ZIP Code', type: 'text' },
          { field: 'email', placeholder: 'Your email', type: 'email' }
        ].map(({ field, placeholder, type }) => (
          <div key={field} className="form-group">
            <input
              type={type}
              className={errors[field] ? 'form-control error' : 'form-control'}
              placeholder={placeholder}
              value={formData[field]}
              onChange={(e) => handleChange(field, e.target.value)}
            />
            {errors[field] && <div className="error-msg">{errors[field]}</div>}
          </div>
        ))}
        
        <div className="form-group">
          <textarea
            className={errors.description ? 'form-control error' : 'form-control'}
            placeholder="Description (include details like color, size, distinguishing features)"
            value={formData.description}
            onChange={(e) => handleChange('description', e.target.value)}
            rows="4"
          />
          {errors.description && <div className="error-msg">{errors.description}</div>}
        </div>
        
        <button
          type="submit"
          className="btn-primary"
          disabled={isSubmitting}
          onClick={handleSubmit}
        >
          {isSubmitting ? 'Submitting...' : 'Submit Report'}
        </button>
      </div>

      {/* Preserve original todo list functionality: display submitted records */}
      {submittedReports.length > 0 && (
        <div className="submitted-reports">
          <h2>Your Submitted Reports</h2>
          <div className="reports-list">
            {submittedReports.map((report) => (
              <div key={report.id} className="report-card">
                <div className="report-header">
                  <h3>{report.title}</h3>
                  <span className={`badge ${report.type}`}>{report.type}</span>
                </div>
                <p><strong>Location:</strong> {report.address}, {report.city} {report.zipCode}</p>
                <p><strong>Description:</strong> {report.description}</p>
                <p><strong>Contact:</strong> {report.email}</p>
                <p className="submitted-time">Submitted: {report.submittedAt}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

// All Items Page
const AllItemsPage = ({ navigate, allItems }) => {
  const [filter, setFilter] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');
  
  useEffect(() => { document.title = 'All Items - Lost & Found'; }, []);
  
  const filteredItems = allItems.filter(item => {
    const matchesFilter = filter === 'all' || item.type === filter;
    const matchesSearch = [item.title, item.location, item.description]
      .some(text => text.toLowerCase().includes(searchTerm.toLowerCase()));
    return matchesFilter && matchesSearch;
  });
  
  return (
    <div className="page">
      <h1>All Items</h1>
      
      <div className="filters">
        <input
          type="text"
          className="search-input"
          placeholder="Search items..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        
        {['all', 'lost', 'found'].map(filterType => (
          <button
            key={filterType}
            className={filter === filterType ? 'filter-btn active' : 'filter-btn'}
            onClick={() => setFilter(filterType)}
          >
            {filterType === 'all' ? 'All Items' : filterType.charAt(0).toUpperCase() + filterType.slice(1)}
          </button>
        ))}
      </div>
      
      <p className="results-count">
        Showing {filteredItems.length} item{filteredItems.length !== 1 ? 's' : ''}
      </p>
      
      {filteredItems.length === 0 ? (
        <div className="no-results">No items found matching your search criteria.</div>
      ) : (
        filteredItems.map(item => (
          <div key={item.id} className="item-card">
            <div className="item-header">
              <h3>{item.title}</h3>
              <span className={`badge ${item.type}`}>{item.type}</span>
            </div>
            <p><strong>Location:</strong> {item.location}</p>
            <p><strong>Date:</strong> {item.date}</p>
            <p><strong>Description:</strong> {item.description}</p>
            {item.email && <p><strong>Contact:</strong> {item.email}</p>}
          </div>
        ))
      )}
    </div>
  );
};

// Login Page
const LoginPage = ({ navigate, setIsLoggedIn, setUser }) => {
  const [isRegistering, setIsRegistering] = useState(false);
  const [formData, setFormData] = useState({ username: '', password: '' });
  const [error, setError] = useState('');

  useEffect(() => {
    document.title = isRegistering ? 'Register - Lost & Found' : 'Login - Lost & Found';
  }, [isRegistering]);

  const handleChange = (field, value) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
    if (error) setError('');
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const { username, password } = formData;

    if (!username || !password) {
      setError('Please fill in all fields.');
      return;
    }

    // For demo purposes, we'll use simple hardcoded authentication
    // In a real app, this would be handled by a backend API
    const users = { 'user': 'password', 'admin': 'admin123' };

    if (isRegistering) {
      // In a real app, this would create a new user account
      alert('Registration successful! Please use username "user" and password "password" to login.');
      setIsRegistering(false);
      setFormData({ username: '', password: '' });
    } else {
      if (users[username] !== password) {
        setError('Invalid username or password. Try: user/password');
        return;
      }
      setUser(username);
      setIsLoggedIn(true);
      navigate('/');
    }
  };

  return (
    <div className="page">
      <h1>{isRegistering ? 'Register' : 'Login'}</h1>
      <form className="form" onSubmit={handleSubmit}>
        <div className="form-group">
          <input
            type="text"
            className="form-control"
            placeholder="Username"
            value={formData.username}
            onChange={(e) => handleChange('username', e.target.value)}
          />
        </div>
        <div className="form-group">
          <input
            type="password"
            className="form-control"
            placeholder="Password"
            value={formData.password}
            onChange={(e) => handleChange('password', e.target.value)}
          />
        </div>
        {error && <div className="error-msg">{error}</div>}
        <button type="submit" className="btn-primary">
          {isRegistering ? 'Register' : 'Login'}
        </button>
      </form>
      <p>
        {isRegistering ? 'Already have an account?' : "Don't have an account?"}{' '}
        <span
          className="link"
          onClick={() => setIsRegistering((prev) => !prev)}
        >
          {isRegistering ? 'Login' : 'Register'}
        </span>
      </p>
      {!isRegistering && (
        <div style={{ marginTop: '1rem', padding: '1rem', background: '#f0f0f0', borderRadius: '4px' }}>
          <small>Demo credentials: username "user", password "password"</small>
        </div>
      )}
    </div>
  );
};

// About Page
const AboutPage = ({ navigate }) => {
  useEffect(() => { document.title = 'About - Lost & Found'; }, []);
  
  return (
    <div className="page">
      <h1>About</h1>
      <p>This project was developed as part of ACIS 498: Information Systems Capstone.</p>
      <p>It is designed to help people report and find lost items more easily and efficiently.</p>
      <p style={{ marginTop: '2rem' }}>
        <strong>Contact:</strong><br />
        Jiani Wang<br />
        <a href="mailto:jianiwang2024@u.northwestern.edu">jianiwang2024@u.northwestern.edu</a>
      </p>
    </div>
  );
};

// Main App
const App = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState(null);
  const [allItems, setAllItems] = useState([
    {
      id: 1,
      title: 'Black Umbrella',
      location: 'Pritzker Legal Research Center',
      date: 'July 5',
      type: 'found',
      description: 'Black umbrella found near entrance',
      email: 'finder@example.com',
    },
    {
      id: 2,
      title: 'Blue Jacket',
      location: '356-350 E Chicago Ave',
      date: 'July 3',
      type: 'lost',
      description: 'Blue denim jacket, size M',
      email: 'owner@example.com',
    },
  ]);

  const handleLogout = () => {
    setIsLoggedIn(false);
    setUser(null);
  };

  const handleAddItem = (newItem) => {
    setAllItems((prevItems) => [...prevItems, newItem]);
  };

  return (
    <div className="app">
      <style jsx>{`
        .app {
          font-family: Arial, sans-serif;
          margin: 0;
          background: white;
        }
        
        .nav {
          background: #4e2a84;
          color: white;
          padding: 1rem;
          text-align: center;
        }
        
        .nav strong {
          font-size: 1.5rem;
          margin-right: 2rem;
        }
        
        .nav-link {
          color: white;
          margin: 0 1rem;
          padding: 0.5rem 1rem;
          cursor: pointer;
          display: inline-block;
        }
        
        .nav-link.active {
          background: #3a1f62;
        }
        
        .page {
          padding: 2rem;
          text-align: center;
          max-width: 800px;
          margin: 0 auto;
        }
        
        .page h1 {
          color: #4e2a84;
          margin-bottom: 1rem;
        }
        
        .btn-primary {
          background: #4e2a84;
          color: white;
          border: none;
          padding: 12px 24px;
          cursor: pointer;
          font-size: 16px;
          margin: 1rem 0;
        }
        
        .btn-primary:disabled {
          background: gray;
          cursor: not-allowed;
        }
        
        .recent-items {
          margin-top: 3rem;
        }
        
        .item-card {
          background: lightgray;
          padding: 1.5rem;
          margin: 1rem 0;
          border: 1px solid black;
          text-align: left;
        }
        
        .item-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 1rem;
        }
        
        .item-header h3 {
          color: #4e2a84;
          margin: 0;
        }
        
        .badge {
          padding: 4px 12px;
          font-size: 12px;
          text-transform: uppercase;
          font-weight: bold;
          color: white;
        }
        
        .badge.lost {
          background: red;
        }
        
        .badge.found {
          background: green;
        }
        
        .date {
          color: gray;
          font-size: 14px;
        }
        
        .form {
          background: lightgray;
          padding: 2rem;
          border: 2px solid #4e2a84;
          text-align: left;
        }
        
        .form-group {
          margin-bottom: 1rem;
        }
        
        .form-control {
          width: 100%;
          padding: 12px;
          border: 2px solid gray;
          font-size: 16px;
          box-sizing: border-box;
        }
        
        .form-control.error {
          border-color: red;
        }
        
        .error-msg {
          color: red;
          font-size: 14px;
          margin-top: 5px;
        }
        
        .filters {
          display: flex;
          gap: 1rem;
          margin-bottom: 2rem;
          flex-wrap: wrap;
          justify-content: center;
        }
        
        .search-input {
          flex: 1;
          min-width: 200px;
          padding: 10px;
          border: 2px solid gray;
          font-size: 16px;
        }
        
        .filter-btn {
          padding: 10px 20px;
          border: none;
          cursor: pointer;
          font-size: 14px;
          background: lightgray;
          color: black;
        }
        
        .filter-btn.active {
          background: #4e2a84;
          color: white;
        }
        
        .results-count {
          color: gray;
          margin-bottom: 2rem;
        }
        
        .no-results {
          text-align: center;
          padding: 2rem;
          color: gray;
        }
        
        .submitted-reports {
          margin-top: 3rem;
          text-align: left;
        }
        
        .submitted-reports h2 {
          color: #4e2a84;
          text-align: center;
          margin-bottom: 2rem;
        }
        
        .reports-list {
          display: flex;
          flex-direction: column;
          gap: 1rem;
        }
        
        .report-card {
          background: lightgray;
          padding: 1.5rem;
          border: 1px solid black;
        }
        
        .report-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 1rem;
        }
        
        .report-header h3 {
          color: #4e2a84;
          margin: 0;
        }
        
        .submitted-time {
          color: gray;
          font-size: 14px;
          font-style: italic;
          margin-top: 1rem;
        }
        
        .link {
          color: #4e2a84;
          cursor: pointer;
          text-decoration: underline;
        }
        
        @media (max-width: 600px) {
          .filters {
            flex-direction: column;
          }
          
          .search-input {
            min-width: 100%;
          }
        }
      `}</style>
      
      <Router isLoggedIn={isLoggedIn} setIsLoggedIn={setIsLoggedIn}>
        <Navigation isLoggedIn={isLoggedIn} onLogout={handleLogout} />
        <Route path="/" component={HomePage} allItems={allItems} />
        <Route path="/about" component={AboutPage} />
        <Route path="/report" component={ReportPage} onAddItem={handleAddItem} />
        <Route path="/items" component={AllItemsPage} allItems={allItems} />
        <Route path="/login" component={LoginPage} setIsLoggedIn={setIsLoggedIn} setUser={setUser} />
      </Router>
    </div>
  );
};

export default App;