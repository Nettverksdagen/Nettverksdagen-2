import { describe, it, expect, vi, beforeEach } from 'vitest'
import { businesses } from '@/store/businesses.module.js'

describe('businesses store', () => {
  let state

  beforeEach(() => {
    state = { all: [], loaded: false, loading: false }
  })

  describe('mutations', () => {
    it('fetchRequest sets loading state', () => {
      businesses.mutations.fetchRequest(state)
      expect(state.loading).toBe(true)
      expect(state.loaded).toBe(false)
    })

    it('fetchSuccessful sets all and flags', () => {
      const data = [{ id: 1 }]
      businesses.mutations.fetchSuccessful(state, data)
      expect(state.all).toEqual(data)
      expect(state.loading).toBe(false)
      expect(state.loaded).toBe(true)
    })

    it('addBusiness pushes a new business', () => {
      businesses.mutations.addBusiness(state, { id: 1 })
      expect(state.all).toEqual([{ id: 1 }])
    })

    it('deleteBusiness removes a business by id', () => {
      state.all = [{ id: 1 }, { id: 2 }]
      businesses.mutations.deleteBusiness(state, { id: 1 })
      expect(state.all).toEqual([{ id: 2 }])
    })

    it('updateBusiness updates a business by id', () => {
      state.all = [{ id: 1, name: 'old' }]
      businesses.mutations.updateBusiness(state, { id: 1, name: 'new' })
      expect(state.all[0].name).toBe('new')
    })
  })

  describe('actions', () => {
    it('fetchBusinesses commits success on success', async () => {
      const commit = vi.fn()
      global.fetch = vi.fn().mockResolvedValue({
        json: () => Promise.resolve([{ id: 1 }])
      })

      await businesses.actions.fetchBusinesses({ commit })
      expect(commit).toHaveBeenCalledWith('fetchRequest')
      expect(commit).toHaveBeenCalledWith('fetchSuccessful', [{ id: 1 }])
    })

    it('fetchBusinesses commits failure on error', async () => {
      const commit = vi.fn()
      global.fetch = vi.fn().mockRejectedValue(new Error('fail'))

      await businesses.actions.fetchBusinesses({ commit })
      expect(commit).toHaveBeenCalledWith('fetchRequest')
      expect(commit).toHaveBeenCalledWith('fetchFailure', expect.any(Error))
    })
  })

  describe('getters', () => {
    it('levels organizes businesses by level', () => {
      const testState = {
        all: [
          { id: 1, level: 'Hovedsamarbeidspartner' },
          { id: 2, level: 'Gull' },
          { id: 3, level: 'Sølv' }
        ]
      }
      const result = businesses.getters.levels(testState)
      expect(result.find(l => l.level === 'Hovedsamarbeidspartner').businesses).toEqual([{ id: 1, level: 'Hovedsamarbeidspartner' }])
      expect(result.find(l => l.level === 'Gull').businesses).toEqual([{ id: 2, level: 'Gull' }])
      expect(result.find(l => l.level === 'Sølv').businesses).toEqual([{ id: 3, level: 'Sølv' }])
    })

    it('days organizes businesses by level and day', () => {
      const testState = {
        all: [
          { id: 1, level: 'Hovedsamarbeidspartner', days: 'Dag 1' },
          { id: 2, level: 'Gull', days: 'Dag 2' },
          { id: 3, level: 'Sølv', days: 'Begge dager' }
        ]
      }
      const result = businesses.getters.days(testState)
      const day1Levels = result.find(d => d.day === 'Dag 1').levels
      const day2Levels = result.find(d => d.day === 'Dag 2').levels

      expect(day1Levels.find(l => l.level === 'Hovedsamarbeidspartner').businesses).toEqual([{ id: 1, level: 'Hovedsamarbeidspartner', days: 'Dag 1' }])
      expect(day1Levels.find(l => l.level === 'Sølv').businesses).toEqual([{ id: 3, level: 'Sølv', days: 'Begge dager' }])

      expect(day2Levels.find(l => l.level === 'Gull').businesses).toEqual([{ id: 2, level: 'Gull', days: 'Dag 2' }])
      expect(day2Levels.find(l => l.level === 'Sølv').businesses).toEqual([{ id: 3, level: 'Sølv', days: 'Begge dager' }])
    })
  })
})

