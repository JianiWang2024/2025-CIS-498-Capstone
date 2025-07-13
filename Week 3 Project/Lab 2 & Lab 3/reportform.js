import { useState } from 'react';

export default function ReportForm() {
  const [form, setForm] = useState({
    type: '',
    title: '',
    address: '',
    city: '',
    zip: '',
    description: '',
    email: ''
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    alert('Report submitted:\n' + JSON.stringify(form, null, 2));
    setForm({
      type: '', title: '', address: '', city: '', zip: '', description: '', email: ''
    });
  };

  return (
    <form onSubmit={handleSubmit} style={formStyle}>
      <h2>Report Lost or Found Item</h2>

      <select name="type" value={form.type} onChange={handleChange} required>
        <option value="">Select Type</option>
        <option value="lost">Lost</option>
        <option value="found">Found</option>
      </select>

      <input type="text" name="title" placeholder="Item title" value={form.title} onChange={handleChange} required />
      <input type="text" name="address" placeholder="Street Address" value={form.address} onChange={handleChange} required />
      <input type="text" name="city" placeholder="City" value={form.city} onChange={handleChange} required />
      <input type="text" name="zip" placeholder="ZIP Code" value={form.zip} onChange={handleChange} required pattern="\d{5}" />
      <textarea name="description" placeholder="Description" value={form.description} onChange={handleChange} required />
      <input type="email" name="email" placeholder="Your email" value={form.email} onChange={handleChange} required />

      <button type="submit">Submit</button>
    </form>
  );
}

const formStyle = {
  maxWidth: '400px',
  margin: '2rem auto',
  background: '#fff',
  padding: '20px',
  borderRadius: '8px',
  border: '2px solid #3399cc'
};
