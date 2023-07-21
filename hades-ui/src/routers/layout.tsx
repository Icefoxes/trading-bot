import React from 'react';
import { Avatar, Button, Layout, Menu, Tooltip, Result, Spin } from 'antd';
import { LoginOutlined } from '@ant-design/icons';
import { Outlet, Link } from 'react-router-dom';
import { useAuth0 } from "@auth0/auth0-react";
import './layout.scss';
import 'ag-grid-community/styles/ag-grid.css'; // Core grid CSS, always needed
import 'ag-grid-community/styles/ag-theme-alpine.css'; // Optional theme CSS

const { Header, Content, } = Layout;

export const BasicLayout: React.FC = () => {
    const { loginWithRedirect, logout, isAuthenticated, user, isLoading } = useAuth0();
    if (isLoading) {
        return <div className='auth-loading-container'><Spin size="large" /></div>
    }
    return (
        <Layout className='hades-layout'>
            <Header style={{ display: 'flex', alignItems: 'center', width: '100vw' }}>
                <div className='logo' />
                <Menu
                    theme='dark'
                    mode='horizontal'
                    className='layout-header-menus'
                    items={[
                        {
                            key: '1',
                            label: <Link to='/market' >Market</Link>
                        }
                    ]} />
                {isAuthenticated && <div className='hades-header-name'>
                    <Tooltip title='logout'><LoginOutlined style={{ color: 'white' }} onClick={() => logout({ logoutParams: { returnTo: window.location.origin } })} /></Tooltip>
                    <span className='hades-header-name-text'>{user?.name}</span>
                    <Avatar src={user?.picture} />
                </div>}

            </Header>
            <Content style={{ width: '100vw' }}>
                <div className='site-layout-content'>
                    {isAuthenticated && <Outlet />}
                    {!isAuthenticated && <Result
                        status="403"
                        title="403"
                        subTitle="Sorry, you are not authorized to access this page."
                        extra={<Button type="primary" onClick={() => loginWithRedirect()}>Login</Button>}
                    />}
                </div>
            </Content>

        </Layout>
    );
};