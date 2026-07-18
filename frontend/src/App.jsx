import { useState, useEffect } from 'react'
import axios from 'axios'

const API_URL = 'http://127.0.0.1:8000'

function App() {
  const [isLogin, setIsLogin] = useState(true)
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [token, setToken] = useState(localStorage.getItem('stir_token') || '')
  const [error, setError] = useState('')

  const [pantry, setPantry] = useState([])
  const [newItem, setNewItem] = useState('')
  const [recipes, setRecipes] = useState([])
  const [loadingRecipes, setLoadingRecipes] = useState(false)

  const authHeader = { headers: { Authorization: `Bearer ${token}` } }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    try {
      const endpoint = isLogin ? '/login' : '/signup'
      const res = await axios.post(`${API_URL}${endpoint}`, { email, password })
      const newToken = res.data.access_token
      setToken(newToken)
      localStorage.setItem('stir_token', newToken)
    } catch (err) {
      setError(err.response?.data?.detail || 'Something went wrong')
    }
  }

  const handleLogout = () => {
    setToken('')
    localStorage.removeItem('stir_token')
    setPantry([])
    setRecipes([])
  }

  const fetchPantry = async () => {
    try {
      const res = await axios.get(`${API_URL}/pantry`, authHeader)
      setPantry(res.data)
    } catch (err) {
      console.error(err)
    }
  }

  const addItem = async (e) => {
    e.preventDefault()
    if (!newItem.trim()) return
    try {
      await axios.post(`${API_URL}/pantry`, { name: newItem.trim() }, authHeader)
      setNewItem('')
      fetchPantry()
    } catch (err) {
      console.error(err)
    }
  }

  const deleteItem = async (id) => {
    try {
      await axios.delete(`${API_URL}/pantry/${id}`, authHeader)
      fetchPantry()
    } catch (err) {
      console.error(err)
    }
  }

  const findRecipes = async () => {
    setLoadingRecipes(true)
    setError('')
    try {
      const res = await axios.get(`${API_URL}/recipes`, authHeader)
      setRecipes(res.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Could not fetch recipes')
    } finally {
      setLoadingRecipes(false)
    }
  }

  useEffect(() => {
    if (token) fetchPantry()
  }, [token])

  if (!token) {
    return (
      <div style={{ padding: '2rem', fontFamily: 'sans-serif', maxWidth: '400px' }}>
        <h1>🍳 Stir</h1>
        <h2>{isLogin ? 'Log In' : 'Sign Up'}</h2>
        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: '1rem' }}>
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              style={{ width: '100%', padding: '0.5rem' }}
              required
            />
          </div>
          <div style={{ marginBottom: '1rem' }}>
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              style={{ width: '100%', padding: '0.5rem' }}
              required
            />
          </div>
          {error && <p style={{ color: 'red' }}>{error}</p>}
          <button type="submit" style={{ padding: '0.5rem 1rem' }}>
            {isLogin ? 'Log In' : 'Sign Up'}
          </button>
        </form>
        <p style={{ marginTop: '1rem' }}>
          {isLogin ? "Don't have an account?" : "Already have an account?"}{' '}
          <button onClick={() => setIsLogin(!isLogin)} style={{ background: 'none', border: 'none', color: 'blue', cursor: 'pointer', textDecoration: 'underline' }}>
            {isLogin ? 'Sign up' : 'Log in'}
          </button>
        </p>
      </div>
    )
  }

  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif', maxWidth: '600px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1>🍳 Stir</h1>
        <button onClick={handleLogout}>Log out</button>
      </div>

      <h2>Your Pantry</h2>
      <form onSubmit={addItem} style={{ display: 'flex', gap: '0.5rem', marginBottom: '1rem' }}>
        <input
          type="text"
          placeholder="e.g. eggs"
          value={newItem}
          onChange={(e) => setNewItem(e.target.value)}
          style={{ flex: 1, padding: '0.5rem' }}
        />
        <button type="submit">Add</button>
      </form>

      <ul style={{ listStyle: 'none', padding: 0 }}>
        {pantry.map((item) => (
          <li key={item.id} style={{ display: 'flex', justifyContent: 'space-between', padding: '0.5rem', borderBottom: '1px solid #eee' }}>
            {item.name}
            <button onClick={() => deleteItem(item.id)} style={{ color: 'red', border: 'none', background: 'none', cursor: 'pointer' }}>
              Remove
            </button>
          </li>
        ))}
      </ul>

      <button onClick={findRecipes} style={{ marginTop: '1.5rem', padding: '0.75rem 1.5rem', fontSize: '1rem' }} disabled={loadingRecipes}>
        {loadingRecipes ? 'Searching...' : '🔍 Find Recipes'}
      </button>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      <div style={{ marginTop: '1.5rem' }}>
        {recipes.map((recipe) => (
          <div key={recipe.id} style={{ border: '1px solid #ddd', borderRadius: '8px', padding: '1rem', marginBottom: '1rem' }}>
            <h3>{recipe.title}</h3>
            <img src={recipe.image} alt={recipe.title} style={{ width: '100%', maxWidth: '300px', borderRadius: '8px' }} />
            <p>✅ Uses: {recipe.usedIngredients.map((i) => i.name).join(', ') || 'none'}</p>
            <p>🛒 Missing: {recipe.missedIngredients.map((i) => i.name).join(', ') || 'none'}</p>
          </div>
        ))}
      </div>
    </div>
  )
}

export default App