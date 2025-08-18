import { useState, useEffect } from 'react'
import axios from 'axios'
import { PlusIcon, PencilIcon, TrashIcon, CheckIcon, XMarkIcon } from '@heroicons/react/24/outline'

function TodoList() {
  const [todos, setTodos] = useState([])
  const [loading, setLoading] = useState(true)
  const [newTodo, setNewTodo] = useState({ title: '', description: '' })
  const [editingTodo, setEditingTodo] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchTodos()
  }, [])

  const fetchTodos = async () => {
    try {
      const response = await axios.get('/todos')
      setTodos(response.data)
    } catch (error) {
      setError('Failed to fetch todos')
    } finally {
      setLoading(false)
    }
  }

  const createTodo = async (e) => {
    e.preventDefault()
    if (!newTodo.title.trim()) return

    try {
      const response = await axios.post('/todos', newTodo)
      setTodos([...todos, response.data])
      setNewTodo({ title: '', description: '' })
      setError('')
    } catch (error) {
      setError('Failed to create todo')
    }
  }

  const updateTodo = async (id, updates) => {
    try {
      const response = await axios.put(`/todos/${id}`, updates)
      setTodos(todos.map(todo => todo.id === id ? response.data : todo))
      setEditingTodo(null)
      setError('')
    } catch (error) {
      setError('Failed to update todo')
    }
  }

  const deleteTodo = async (id) => {
    try {
      await axios.delete(`/todos/${id}`)
      setTodos(todos.filter(todo => todo.id !== id))
      setError('')
    } catch (error) {
      setError('Failed to delete todo')
    }
  }

  const toggleComplete = async (todo) => {
    await updateTodo(todo.id, { completed: !todo.completed })
  }

  const startEditing = (todo) => {
    setEditingTodo({
      id: todo.id,
      title: todo.title,
      description: todo.description || ''
    })
  }

  const saveEdit = async () => {
    if (!editingTodo.title.trim()) return
    await updateTodo(editingTodo.id, {
      title: editingTodo.title,
      description: editingTodo.description
    })
  }

  const cancelEdit = () => {
    setEditingTodo(null)
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
      <div className="bg-white rounded-lg shadow-sm border">
        {/* Header */}
        <div className="px-6 py-4 border-b">
          <h2 className="text-2xl font-bold text-gray-900">My Todos</h2>
        </div>

        {/* Add Todo Form */}
        <div className="px-6 py-4 border-b bg-gray-50">
          <form onSubmit={createTodo} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <input
                type="text"
                placeholder="Todo title..."
                value={newTodo.title}
                onChange={(e) => setNewTodo({ ...newTodo, title: e.target.value })}
                className="px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                required
              />
              <input
                type="text"
                placeholder="Description (optional)..."
                value={newTodo.description}
                onChange={(e) => setNewTodo({ ...newTodo, description: e.target.value })}
                className="px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <button
              type="submit"
              className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors"
            >
              <PlusIcon className="w-5 h-5 mr-2" />
              Add Todo
            </button>
          </form>
        </div>

        {/* Error Message */}
        {error && (
          <div className="px-6 py-3 bg-red-50 border-b">
            <div className="text-red-700 text-sm">{error}</div>
          </div>
        )}

        {/* Todo List */}
        <div className="divide-y divide-gray-200">
          {todos.length === 0 ? (
            <div className="px-6 py-8 text-center text-gray-500">
              <p>No todos yet. Create your first todo above!</p>
            </div>
          ) : (
            todos.map((todo) => (
              <div key={todo.id} className="px-6 py-4">
                {editingTodo && editingTodo.id === todo.id ? (
                  // Edit Mode
                  <div className="space-y-3">
                    <input
                      type="text"
                      value={editingTodo.title}
                      onChange={(e) => setEditingTodo({ ...editingTodo, title: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                    <input
                      type="text"
                      value={editingTodo.description}
                      onChange={(e) => setEditingTodo({ ...editingTodo, description: e.target.value })}
                      placeholder="Description..."
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                    <div className="flex space-x-2">
                      <button
                        onClick={saveEdit}
                        className="inline-flex items-center px-3 py-1 bg-green-600 text-white rounded-md hover:bg-green-700 text-sm"
                      >
                        <CheckIcon className="w-4 h-4 mr-1" />
                        Save
                      </button>
                      <button
                        onClick={cancelEdit}
                        className="inline-flex items-center px-3 py-1 bg-gray-600 text-white rounded-md hover:bg-gray-700 text-sm"
                      >
                        <XMarkIcon className="w-4 h-4 mr-1" />
                        Cancel
                      </button>
                    </div>
                  </div>
                ) : (
                  // Display Mode
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3 flex-1">
                      <input
                        type="checkbox"
                        checked={todo.completed}
                        onChange={() => toggleComplete(todo)}
                        className="h-5 w-5 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                      />
                      <div className="flex-1">
                        <h3 className={`text-lg font-medium ${todo.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
                          {todo.title}
                        </h3>
                        {todo.description && (
                          <p className={`text-sm ${todo.completed ? 'line-through text-gray-400' : 'text-gray-600'}`}>
                            {todo.description}
                          </p>
                        )}
                        <p className="text-xs text-gray-400 mt-1">
                          Created: {new Date(todo.created_at).toLocaleDateString()}
                        </p>
                      </div>
                    </div>
                    <div className="flex space-x-2">
                      <button
                        onClick={() => startEditing(todo)}
                        className="p-2 text-gray-400 hover:text-blue-600 transition-colors"
                      >
                        <PencilIcon className="w-5 h-5" />
                      </button>
                      <button
                        onClick={() => deleteTodo(todo.id)}
                        className="p-2 text-gray-400 hover:text-red-600 transition-colors"
                      >
                        <TrashIcon className="w-5 h-5" />
                      </button>
                    </div>
                  </div>
                )}
              </div>
            ))
          )}
        </div>

        {/* Footer */}
        {todos.length > 0 && (
          <div className="px-6 py-3 bg-gray-50 text-sm text-gray-600">
            Total: {todos.length} todos • Completed: {todos.filter(t => t.completed).length} • 
            Pending: {todos.filter(t => !t.completed).length}
          </div>
        )}
      </div>
    </div>
  )
}

export default TodoList 