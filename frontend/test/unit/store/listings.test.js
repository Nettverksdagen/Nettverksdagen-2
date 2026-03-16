import { describe, it, expect, vi, beforeEach } from 'vitest'
import { listings } from '@/store/listings.module.js'

describe('listings store', () => {
  let state

  beforeEach(() => {
    state = { all: [], loaded: false, loading: false }
  })

  describe('mutations', () => {
    it('fetchRequest sets loading state', () => {
      listings.mutations.fetchRequest(state)
      expect(state.loading).toBe(true)
      expect(state.loaded).toBe(false)
    })

    it('fetchSuccessful sets all and flags', () => {
      const data = [{ id: 1 }]
      listings.mutations.fetchSuccessful(state, data)
      expect(state.all).toEqual(data)
      expect(state.loading).toBe(false)
      expect(state.loaded).toBe(true)
    })

    it('addListing pushes a new listing', () => {
      listings.mutations.addListing(state, { id: 1 })
      expect(state.all).toEqual([{ id: 1 }])
    })

    it('deleteListing removes a listing by id', () => {
      state.all = [{ id: 1 }, { id: 2 }]
      listings.mutations.deleteListing(state, { id: 1 })
      expect(state.all).toEqual([{ id: 2 }])
    })

    it('updateListing updates a listing by id', () => {
      state.all = [{ id: 1, title: 'old' }]
      listings.mutations.updateListing(state, { id: 1, title: 'new' })
      expect(state.all[0].title).toBe('new')
    })
  })

  describe('actions', () => {
    it('fetchListings commits success on success', async () => {
      const commit = vi.fn()
      global.fetch = vi.fn().mockResolvedValue({
        json: () => Promise.resolve([{ id: 1 }])
      })

      await listings.actions.fetchListings({ commit })
      expect(commit).toHaveBeenCalledWith('fetchRequest')
      expect(commit).toHaveBeenCalledWith('fetchSuccessful', [{ id: 1 }])
    })

    it('fetchListings commits failure on error', async () => {
      const commit = vi.fn()
      global.fetch = vi.fn().mockRejectedValue(new Error('fail'))

      await listings.actions.fetchListings({ commit })
      expect(commit).toHaveBeenCalledWith('fetchRequest')
      expect(commit).toHaveBeenCalledWith('fetchFailure', expect.any(Error))
    })
  })
})
