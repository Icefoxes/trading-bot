import { marketApi } from './market.service';
import { commissionApi } from './commission.service';

export * from './market.service';
export * from './commission.service';

export const ServiceMiddlewares = [commissionApi.middleware, marketApi.middleware]
export const ServiceReducers = {
    [marketApi.reducerPath]: marketApi.reducer,
    [commissionApi.reducerPath]: commissionApi.reducer,
}
