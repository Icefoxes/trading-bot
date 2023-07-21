import React from 'react';
import { Avatar, Button, Layout, Menu, Tooltip, Result } from 'antd';
import { LoginOutlined, LogoutOutlined } from '@ant-design/icons';
import { Outlet, Link, useNavigate } from 'react-router-dom';
import { useAuth0 } from "@auth0/auth0-react";

const { Header, Content, } = Layout;

export const BasicLayout: React.FC = () => {
    const { loginWithRedirect, logout, isAuthenticated, user } = useAuth0();
    const navigate = useNavigate();
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
                {isAuthenticated && <>
                    <Tooltip title='logout'><Button type="primary" onClick={() => logout({ logoutParams: { returnTo: window.location.origin } })} icon={<LoginOutlined />} /></Tooltip>
                    <Avatar src={user?.picture} />
                </>}
                {!isAuthenticated && <Tooltip title='login'><Button type="primary" onClick={() => loginWithRedirect()} icon={<LogoutOutlined />} /></Tooltip>}

            </Header>
            <Content style={{ padding: '0 50px', height: '100%' }}>
                <div className='site-layout-content'>
                    {isAuthenticated && <Outlet />}
                    {!isAuthenticated && <Result
                        status="403"
                        title="403"
                        subTitle="Sorry, you are not authorized to access this page."
                        extra={<Button type="primary" onClick={() => navigate('/')}>Back Home</Button>}
                    />}
                </div>
            </Content>

        </Layout>
    );
};