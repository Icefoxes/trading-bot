import React from 'react';
import { Avatar, Layout, Menu } from 'antd';
import { Outlet, Link } from 'react-router-dom';

const { Header, Content, Footer } = Layout;

export const BasicLayout: React.FC = () => {
    return (
        <Layout className='layout'>
            <Header style={{ display: 'flex', alignItems: 'center', width: '100vw' }}>
                <div className='demo-logo' />
                <Menu
                    theme='dark'
                    mode='horizontal'
                    style={{ 'width': '100vw' }}
                    defaultSelectedKeys={['1']}
                    items={[
                        {
                            key: '1',
                            label: <Link to='/klines/1m' >1m</Link>
                        },
                        {
                            key: '2',
                            label: <Link to='/klines/5m'>5m</Link>
                        },
                        {
                            key: '3',
                            label: <Link to='/klines/15m'>15m</Link>
                        }
                    ]} />
                <Avatar src='https://xsgames.co/randomusers/avatar.php?g=pixel&key=2' />
            </Header>
            <Content style={{ padding: '0 50px' }}>
                <div className='site-layout-content'>
                    <Outlet />
                </div>
            </Content>
            <Footer style={{ textAlign: 'center' }}>Trading Bot</Footer>
        </Layout>
    );
};