import { describe, it, expect, vi, beforeEach } from 'vitest'
import { forms } from '@/store/forms.module.js'

describe('forms store', () => {
  let state

  beforeEach(() => {
    state = { all: [], loaded: false, loading: false }
  })

  describe('mutations', () => {
    it('fetchRequest sets loading state', () => {
      forms.mutations.fetchRequest(state)
      expect(state.loading).toBe(true)
      expect(state.loaded).toBe(false)
    })

    it('fetchSuccessful sets all and flags', () => {
      const data = [{ id: 1 }]
      forms.mutations.fetchSuccessful(state, data)
      expect(state.all).toEqual(data)
      expect(state.loading).toBe(false)
      expect(state.loaded).toBe(true)
    })

    it('addForm pushes a new form', () => {
      forms.mutations.addForm(state, { id: 1 })
      expect(state.all).toEqual([{ id: 1 }])
    })

    it('deleteForm removes a form by id', () => {
      state.all = [{ id: 1 }, { id: 2 }]
      forms.mutations.deleteForm(state, { id: 1 })
      expect(state.all).toEqual([{ id: 2 }])
    })

    it('updateForm updates a form by id', () => {
      state.all = [{ id: 1, title: 'old' }]
      forms.mutations.updateForm(state, { id: 1, title: 'new' })
      expect(state.all[0].title).toBe('new')
    })
  })

  describe('actions', () => {
    it('fetchForms commits success on success', async () => {
      const commit = vi.fn()
      global.fetch = vi.fn().mockResolvedValue({
        json: () => Promise.resolve([{ id: 1 }])
      })

      await forms.actions.fetchForms({ commit })
      expect(commit).toHaveBeenCalledWith('fetchRequest')
      expect(commit).toHaveBeenCalledWith('fetchSuccessful', [{ id: 1 }])
    })

    it('fetchForms commits failure on error', async () => {
      const commit = vi.fn()
      global.fetch = vi.fn().mockRejectedValue(new Error('fail'))

      await forms.actions.fetchForms({ commit })
      expect(commit).toHaveBeenCalledWith('fetchRequest')
      expect(commit).toHaveBeenCalledWith('fetchFailure', expect.any(Error))
    })
  })

  describe('getters', () => {
    it('form returns the correct form by internal_url', () => {
      const testState = {
        all: [
          { id: 1, internal_url: 'form-a' },
          { id: 2, internal_url: 'form-b' }
        ]
      }
      const getter = forms.getters.form(testState)
      expect(getter('form-a')).toEqual({ id: 1, internal_url: 'form-a' })
      expect(getter('form-b')).toEqual({ id: 2, internal_url: 'form-b' })
      expect(getter('nonexistent')).toBeNull()
    })
  })
})

