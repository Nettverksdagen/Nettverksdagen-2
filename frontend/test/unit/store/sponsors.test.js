import { describe, it, expect, vi, beforeEach } from 'vitest'
import { sponsors } from '@/store/sponsors.module.js'

describe('sponsors store', () => {
  let state

  beforeEach(() => {
    state = { all: [], loaded: false, loading: false }
  })

  describe('mutations', () => {
    it('fetchRequest sets loading state', () => {
      sponsors.mutations.fetchRequest(state)
      expect(state.loading).toBe(true)
      expect(state.loaded).toBe(false)
    })

    it('fetchSuccessful sets all and flags', () => {
      const sponsorData = [{ id: 1 }]
      sponsors.mutations.fetchSuccessful(state, sponsorData)
      expect(state.all).toEqual(sponsorData)
      expect(state.loading).toBe(false)
      expect(state.loaded).toBe(true)
    })

    it('addSponsor pushes a new sponsor', () => {
      sponsors.mutations.addSponsor(state, { id: 1 })
      expect(state.all).toEqual([{ id: 1 }])
    })

    it('deleteSponsor removes a sponsor by id', () => {
      state.all = [{ id: 1 }, { id: 2 }]
      sponsors.mutations.deleteSponsor(state, { id: 1 })
      expect(state.all).toEqual([{ id: 2 }])
    })

    it('updateSponsor updates a sponsor by id', () => {
      state.all = [{ id: 1, name: 'old' }]
      sponsors.mutations.updateSponsor(state, { id: 1, name: 'new' })
      expect(state.all[0].name).toBe('new')
    })
  })

  describe('actions', () => {
    it('fetchSponsors commits success on success', async () => {
      const commit = vi.fn()
      global.fetch = vi.fn().mockResolvedValue({
        json: () => Promise.resolve([{ id: 1 }])
      })

      await sponsors.actions.fetchSponsors({ commit })
      expect(commit).toHaveBeenCalledWith('fetchRequest')
      expect(commit).toHaveBeenCalledWith('fetchSuccessful', [{ id: 1 }])
    })

    it('fetchSponsors commits failure on error', async () => {
      const commit = vi.fn()
      global.fetch = vi.fn().mockRejectedValue(new Error('fail'))

      await sponsors.actions.fetchSponsors({ commit })
      expect(commit).toHaveBeenCalledWith('fetchRequest')
      expect(commit).toHaveBeenCalledWith('fetchFailure', expect.any(Error))
    })
  })
})
