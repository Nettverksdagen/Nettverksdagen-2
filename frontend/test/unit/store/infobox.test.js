import { describe, it, expect, vi, beforeEach } from 'vitest'
import { infobox } from '@/store/infobox.module.js'

describe('infobox store', () => {
  let state

  beforeEach(() => {
    state = { title_nb: null, title_en: null, paragraph_nb: null, paragraph_en: null, loaded: false, loading: false }
  })

  describe('mutations', () => {
    it('fetchRequest sets loading state', () => {
      infobox.mutations.fetchRequest(state)
      expect(state.loading).toBe(true)
      expect(state.loaded).toBe(false)
    })

    it('fetchSuccessful sets all fields and flags', () => {
      const data = { 
        title_nb: 'Viktig informasjon', 
        title_en: 'Important information',
        paragraph_nb: 'Les dette',
        paragraph_en: 'Read this'
      }
      infobox.mutations.fetchSuccessful(state, data)
      expect(state.title_nb).toBe('Viktig informasjon')
      expect(state.title_en).toBe('Important information')
      expect(state.paragraph_nb).toBe('Les dette')
      expect(state.paragraph_en).toBe('Read this')
      expect(state.loading).toBe(false)
      expect(state.loaded).toBe(true)
    })
  })

  describe('actions', () => {
    it('fetchInfobox commits success on success', async () => {
      const commit = vi.fn()
      global.fetch = vi.fn().mockResolvedValue({
        json: () => Promise.resolve([{ 
          title_nb: 'Test', 
          title_en: 'Test',
          paragraph_nb: 'Text',
          paragraph_en: 'Text'
        }])
      })

      await infobox.actions.fetchInfobox({ commit })
      expect(commit).toHaveBeenCalledWith('fetchRequest')
      expect(commit).toHaveBeenCalledWith('fetchSuccessful', expect.objectContaining({ title_nb: 'Test' }))
    })

    it('fetchInfobox commits failure on error', async () => {
      const commit = vi.fn()
      global.fetch = vi.fn().mockRejectedValue(new Error('fail'))

      await infobox.actions.fetchInfobox({ commit })
      expect(commit).toHaveBeenCalledWith('fetchRequest')
      expect(commit).toHaveBeenCalledWith('fetchFailure', expect.any(Error))
    })
  })
})
