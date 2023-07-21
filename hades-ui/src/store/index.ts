import { configureStore } from '@reduxjs/toolkit';
import { ServiceReducers, ServiceMiddlewares } from '../services';

export const store = configureStore({
  reducer: {
    ...ServiceReducers
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat([...ServiceMiddlewares]),
})

// Infer the `RootState` and `AppDispatch` types from the store itself
export type RootState = ReturnType<typeof store.getState>
// Inferred type: {posts: PostsState, comments: CommentsState, users: UsersState}
export type AppDispatch = typeof store.dispatch