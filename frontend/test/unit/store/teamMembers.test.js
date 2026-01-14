import { describe, it, expect, vi, beforeEach } from 'vitest'
import { teamMembers } from '@/store/teamMembers.module.js'

describe('teamMembers store', () => {
  let state

  beforeEach(() => {
    state = { all: [], loaded: false, loading: false }
  })

  describe('mutations', () => {
    it('fetchRequest sets loading state', () => {
      teamMembers.mutations.fetchRequest(state)
      expect(state.loading).toBe(true)
      expect(state.loaded).toBe(false)
    })

    it('fetchSuccessful sets all and flags', () => {
      const members = [{ id: 1 }]
      teamMembers.mutations.fetchSuccessful(state, members)
      expect(state.all).toEqual(members)
      expect(state.loading).toBe(false)
      expect(state.loaded).toBe(true)
    })

    it('addTeamMember pushes a new member', () => {
      teamMembers.mutations.addTeamMember(state, { id: 1 })
      expect(state.all).toEqual([{ id: 1 }])
    })

    it('deleteTeamMember removes a member by id', () => {
      state.all = [{ id: 1 }, { id: 2 }]
      teamMembers.mutations.deleteTeamMember(state, { id: 1 })
      expect(state.all).toEqual([{ id: 2 }])
    })

    it('updateTeamMember updates a member by id', () => {
      state.all = [{ id: 1, name: 'old' }]
      teamMembers.mutations.updateTeamMember(state, { id: 1, name: 'new' })
      expect(state.all[0].name).toBe('new')
    })
  })

  describe('actions', () => {
    it('fetchTeamMembers commits success on success', async () => {
      const commit = vi.fn()
      global.fetch = vi.fn().mockResolvedValue({
        json: () => Promise.resolve([{ id: 1 }])
      })

      await teamMembers.actions.fetchTeamMembers({ commit })
      expect(commit).toHaveBeenCalledWith('fetchRequest')
      expect(commit).toHaveBeenCalledWith('fetchSuccessful', [{ id: 1 }])
    })

    it('fetchTeamMembers commits failure on error', async () => {
      const commit = vi.fn()
      global.fetch = vi.fn().mockRejectedValue(new Error('fail'))

      await teamMembers.actions.fetchTeamMembers({ commit })
      expect(commit).toHaveBeenCalledWith('fetchRequest')
      expect(commit).toHaveBeenCalledWith('fetchFailure', expect.any(Error))
    })
  })

  describe('getters', () => {
    it('teams groups members by team name', () => {
      const testState = {
        all: [
          { id: 1, team: 'A' },
          { id: 2, team: 'B' },
          { id: 3, team: 'A' }
        ]
      }
      const result = teamMembers.getters.teams(testState)
      expect(Object.keys(result)).toHaveLength(2)
      expect(result['A'].members).toEqual([
        { id: 1, team: 'A' },
        { id: 3, team: 'A' }
      ])
      expect(result['B'].members).toEqual([{ id: 2, team: 'B' }])
    })
  })
})
