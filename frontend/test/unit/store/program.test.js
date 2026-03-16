import { describe, it, expect, vi, beforeEach } from 'vitest'
import { program } from '@/store/program.module.js'

describe('program store', () => {
  let state

  beforeEach(() => {
    state = { all: [], loaded: false, loading: false }
  })

  describe('mutations', () => {
    it('fetchRequest sets loading state', () => {
      program.mutations.fetchRequest(state)
      expect(state.loading).toBe(true)
      expect(state.loaded).toBe(false)
    })

    it('fetchSuccessful sets all and flags', () => {
      const programData = [{ id: 1 }]
      program.mutations.fetchSuccessful(state, programData)
      expect(state.all).toEqual(programData)
      expect(state.loading).toBe(false)
      expect(state.loaded).toBe(true)
    })

    it('addProgramItem pushes a new item', () => {
      program.mutations.addProgramItem(state, { id: 1 })
      expect(state.all).toEqual([{ id: 1 }])
    })

    it('deleteProgramItem removes an item by id', () => {
      state.all = [{ id: 1 }, { id: 2 }]
      program.mutations.deleteProgramItem(state, { id: 1 })
      expect(state.all).toEqual([{ id: 2 }])
    })

    it('updateProgramItem updates an item by id', () => {
      state.all = [{ id: 1, name: 'old' }]
      program.mutations.updateProgramItem(state, { id: 1, name: 'new' })
      expect(state.all[0].name).toBe('new')
    })
  })

  describe('getters', () => {
    it('anonProgram formats items with dates and paragraphs', () => {
      const ts = Math.floor(Date.now() / 1000)
      const testState = {
        all: [{ id: 1, timeStart: ts, paragraph: 'line1\nline2' }]
      }
      const result = program.getters.anonProgram(testState)
      expect(result[0].paragraph).toEqual(['line1', 'line2'])
      expect(result[0].timeStart).toBeInstanceOf(Date)
    })

    it('adminProgram formats time and date strings', () => {
      const ts = new Date('2023-05-10T12:34:00Z').getTime() / 1000
      const testState = { all: [{ id: 1, timeStart: ts, paragraph: 'text' }] }
      const result = program.getters.adminProgram(testState)
      expect(result[0].date).toMatch(/\d{4}-\d{2}-\d{2}/)
      expect(result[0].timeStart).toMatch(/\d{2}:\d{2}/)
    })
  })

  describe('actions', () => {
    it('fetchProgram commits success on success', async () => {
      const commit = vi.fn()
      global.fetch = vi.fn().mockResolvedValue({
        json: () => Promise.resolve([{ id: 1 }])
      })
      await program.actions.fetchProgram({ commit })
      expect(commit).toHaveBeenCalledWith('fetchRequest')
      expect(commit).toHaveBeenCalledWith('fetchSuccessful', [{ id: 1 }])
    })

    it('fetchProgram commits failure on error', async () => {
      const commit = vi.fn()
      global.fetch = vi.fn().mockRejectedValue(new Error('fail'))
      await program.actions.fetchProgram({ commit })
      expect(commit).toHaveBeenCalledWith('fetchRequest')
      expect(commit).toHaveBeenCalledWith('fetchFailure', expect.any(Error))
    })
  })
})

