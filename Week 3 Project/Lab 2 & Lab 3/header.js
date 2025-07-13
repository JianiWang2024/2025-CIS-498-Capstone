import { Link } from 'react-router-dom';

export default function Header() {
  return (
    <nav style={{ background: '#3366cc', color: 'white', padding: '1rem', textAlign: 'center' }}>
      <Link to="/" style={{ color: 'white', marginRight: '1rem' }}>Home</Link>
      <Link to="/report" style={{ color: 'white' }}>Report Item</Link>
    </nav>
  );
}