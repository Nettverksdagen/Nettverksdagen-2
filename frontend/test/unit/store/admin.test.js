import { describe, it, expect, vi, beforeEach } from 'vitest'
import { admin } from '@/store/admin.module.js'

describe('admin store', () => {
  let state

  beforeEach(() => {
    state = { ...admin.state, loggingIn: false }
  })

  describe('mutations', () => {
    it('loggingIn sets loggingIn true', () => {
      admin.mutations.loggingIn(state)
      expect(state.loggingIn).toBe(true)
    })

    it('loggedInSuccessfully updates username, token and flags', () => {
      admin.mutations.loggedInSuccessfully(state, { username: 'user', token: 'abc', loggedIn: true })
      expect(state.username).toBe('user')
      expect(state.token).toBe('abc')
      expect(state.loggedIn).toBe(true)
      expect(state.loggingIn).toBe(false)
    })

    it('loginFailure sets flags to false', () => {
      // Add loggingIn to true so we can test mutation
      state.loggingIn = true
      admin.mutations.loginFailure(state)
      expect(state.loggingIn).toBe(false)
      expect(state.loggedIn).toBe(false)
    })

    it('fetchFailure sets loggingIn false', () => {
      state.loggingIn = true
      admin.mutations.fetchFailure(state, new Error('fail'))
      expect(state.loggingIn).toBe(false)
    })
  })

  describe('actions', () => {
    const credentialObserver = { credentials: { username: 'user', password: 'pass' } }

    it('login commits loggedInSuccessfully on successful login', async () => {
      const commit = vi.fn()
      global.fetch = vi.fn().mockResolvedValue({
        json: () => Promise.resolve({ key: 'token123' })
      })

      await admin.actions.login({ commit }, credentialObserver)
      expect(commit).toHaveBeenCalledWith('loggingIn')
      expect(commit).toHaveBeenCalledWith('loggedInSuccessfully', {
        username: 'user',
        token: 'token123',
        loggedIn: true
      })
    })

    it('login commits loginFailure on invalid credentials', async () => {
      const commit = vi.fn()
      global.fetch = vi.fn().mockResolvedValue({
        json: () => Promise.resolve({ non_field_errors: ['error'] })
      })

      await admin.actions.login({ commit }, credentialObserver)
      expect(commit).toHaveBeenCalledWith('loggingIn')
      expect(commit).toHaveBeenCalledWith('loginFailure')
    })

    it('login commits fetchFailure on network or other error', async () => {
      const commit = vi.fn()
      global.fetch = vi.fn().mockRejectedValue(new Error('network error'))

      await admin.actions.login({ commit }, credentialObserver)
      expect(commit).toHaveBeenCalledWith('loggingIn')
      expect(commit).toHaveBeenCalledWith('fetchFailure', expect.any(Error))
    })
  })
})
