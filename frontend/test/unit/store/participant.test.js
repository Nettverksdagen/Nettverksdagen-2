import { describe, it, expect, vi, beforeEach } from 'vitest'
import { participant } from '@/store/participant.module.js'

describe('participant store', () => {
  let state

  beforeEach(() => {
    state = { all: [], loaded: false, loading: false }
  })

  describe('mutations', () => {
    it('fetchRequest sets loading state', () => {
      participant.mutations.fetchRequest(state)
      expect(state.loading).toBe(true)
      expect(state.loaded).toBe(false)
    })

    it('fetchSuccessful sets all and flags', () => {
      const data = [{ id: 1 }]
      participant.mutations.fetchSuccessful(state, data)
      expect(state.all).toEqual(data)
      expect(state.loading).toBe(false)
      expect(state.loaded).toBe(true)
    })

    it('addParticipant pushes a new participant', () => {
      participant.mutations.addParticipant(state, { id: 1 })
      expect(state.all).toEqual([{ id: 1 }])
    })

    it('deleteParticipant removes a participant by id', () => {
      state.all = [{ id: 1 }, { id: 2 }]
      participant.mutations.deleteParticipant(state, { id: 1 })
      expect(state.all).toEqual([{ id: 2 }])
    })

    it('updateParticipant updates a participant by id', () => {
      state.all = [{ id: 1, name: 'old' }]
      participant.mutations.updateParticipant(state, { id: 1, name: 'new' })
      expect(state.all[0].name).toBe('new')
    })
  })

  describe('actions', () => {
    it('fetchParticipant commits success on success', async () => {
      const commit = vi.fn()
      global.fetch = vi.fn().mockResolvedValue({
        json: () => Promise.resolve([{ id: 1 }])
      })

      await participant.actions.fetchParticipant({ commit })
      expect(commit).toHaveBeenCalledWith('fetchRequest')
      expect(commit).toHaveBeenCalledWith('fetchSuccessful', [{ id: 1 }])
    })

    it('fetchParticipant commits failure on error', async () => {
      const commit = vi.fn()
      global.fetch = vi.fn().mockRejectedValue(new Error('fail'))

      await participant.actions.fetchParticipant({ commit })
      expect(commit).toHaveBeenCalledWith('fetchRequest')
      expect(commit).toHaveBeenCalledWith('fetchFailure', expect.any(Error))
    })
  })
})
