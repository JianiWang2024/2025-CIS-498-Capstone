export default function Home() {
    return (
      <section style={{ padding: '2rem', textAlign: 'center' }}>
        <h1>Welcome to Lost & Found</h1>
        <p>Find or report lost items quickly.</p>
  
        <h2>Recent Items</h2>
        <div style={itemStyle}>
          <h3>Black Umbrella</h3>
          <p>Found at Library - July 5</p>
        </div>
        <div style={itemStyle}>
          <h3>Blue Jacket</h3>
          <p>Lost in Cafeteria - July 3</p>
        </div>
      </section>
    );
  }
  
  const itemStyle = {
    background: 'white',
    padding: '1rem',
    margin: '1rem auto',
    maxWidth: '400px',
    borderRadius: '5px'
  };
  