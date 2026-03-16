import { describe, it, expect, vi, beforeEach } from 'vitest'
import { faq } from '@/store/faq.module.js'

describe('faq store', () => {
  let state

  beforeEach(() => {
    state = { all: [], loaded: false, loading: false }
  })

  describe('mutations', () => {
    it('fetchRequest sets loading state', () => {
      faq.mutations.fetchRequest(state)
      expect(state.loading).toBe(true)
      expect(state.loaded).toBe(false)
    })

    it('fetchSuccessful sets all and flags', () => {
      const data = [{ id: 1, question_nb: 'Hva?' }]
      faq.mutations.fetchSuccessful(state, data)
      expect(state.all).toEqual(data)
      expect(state.loading).toBe(false)
      expect(state.loaded).toBe(true)
    })

    it('addFAQ pushes a new faq', () => {
      faq.mutations.addFAQ(state, { id: 1, question_nb: 'Hvorfor?' })
      expect(state.all).toEqual([{ id: 1, question_nb: 'Hvorfor?' }])
    })

    it('deleteFAQ removes a faq by id', () => {
      state.all = [{ id: 1 }, { id: 2 }]
      faq.mutations.deleteFAQ(state, { id: 1 })
      expect(state.all).toEqual([{ id: 2 }])
    })

    it('updateFAQ updates a faq by id', () => {
      state.all = [{ id: 1, question_nb: 'old' }]
      faq.mutations.updateFAQ(state, { id: 1, question_nb: 'new' })
      expect(state.all[0].question_nb).toBe('new')
    })
  })

  describe('actions', () => {
    it('fetchFAQs commits success on success', async () => {
      const commit = vi.fn()
      global.fetch = vi.fn().mockResolvedValue({
        json: () => Promise.resolve([{ id: 1 }])
      })

      await faq.actions.fetchFAQs({ commit })
      expect(commit).toHaveBeenCalledWith('fetchRequest')
      expect(commit).toHaveBeenCalledWith('fetchSuccessful', [{ id: 1 }])
    })

    it('fetchFAQs commits failure on error', async () => {
      const commit = vi.fn()
      global.fetch = vi.fn().mockRejectedValue(new Error('fail'))

      await faq.actions.fetchFAQs({ commit })
      expect(commit).toHaveBeenCalledWith('fetchRequest')
      expect(commit).toHaveBeenCalledWith('fetchFailure', expect.any(Error))
    })
  })
})
